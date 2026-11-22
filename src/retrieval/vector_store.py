import os
import duckdb
import chromadb
from chromadb.config import Settings

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'autorecall.duckdb')
CHROMA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'chroma_index')

def get_chroma_client():
    os.makedirs(CHROMA_PATH, exist_ok=True)
    return chromadb.PersistentClient(path=CHROMA_PATH)

def index_complaints(max_motorcycles=6000, max_cars=10000):
    """
    Indexes clean complaint narratives into persistent ChromaDB.
    Indexes all motorcycle complaints (to prevent signal dilution) and
    a curated subset of high-risk passenger car complaints.
    """
    print(f"Connecting to DuckDB at {DB_PATH}...")
    con = duckdb.connect(DB_PATH, read_only=True)
    
    # Query all motorcycle complaints
    query_moto = f"""
    SELECT CMPLID, MAKETXT, MODELTXT, YEARTXT, COMPDESC, vehicle_category, CRASH, FIRE, CDESCR
    FROM complaints_clean
    WHERE vehicle_category = 'motorcycle' AND CDESCR IS NOT NULL AND length(CDESCR) > 20
    LIMIT {max_motorcycles}
    """
    moto_rows = con.execute(query_moto).fetchall()
    
    # Query high-impact passenger car complaints
    query_cars = f"""
    SELECT CMPLID, MAKETXT, MODELTXT, YEARTXT, COMPDESC, vehicle_category, CRASH, FIRE, CDESCR
    FROM complaints_clean
    WHERE vehicle_category = 'car' AND CDESCR IS NOT NULL AND length(CDESCR) > 20
      AND (MAKETXT IN ('TESLA', 'CHEVROLET', 'HYUNDAI', 'JEEP', 'SUBARU', 'VOLKSWAGEN', 'TOYOTA')
           OR (MAKETXT = 'FORD' AND MODELTXT LIKE '%F-150%')
           OR (MAKETXT = 'HONDA' AND MODELTXT IN ('CR-V', 'CIVIC')))
    LIMIT {max_cars}
    """
    car_rows = con.execute(query_cars).fetchall()
    con.close()
    
    all_rows = moto_rows + car_rows
    print(f"Loaded {len(moto_rows)} motorcycle records and {len(car_rows)} car records (Total: {len(all_rows)}).")
    
    client = get_chroma_client()
    collection_name = "nhtsa_complaints"
    
    # Get or create collection with default ONNX MiniLM embedding function
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    current_count = collection.count()
    if current_count >= len(all_rows) * 0.9:
        print(f"Collection '{collection_name}' already indexed with {current_count} documents.")
        return collection
    
    batch_size = 500
    ids, docs, metadatas = [], [], []
    
    for i, row in enumerate(all_rows):
        cmplid, make, model, year, comp, vcat, crash, fire, text = row
        ids.append(str(cmplid))
        docs.append(f"Make: {make} | Model: {model} ({year}) | Component: {comp} | Description: {text}")
        metadatas.append({
            "cmplid": str(cmplid),
            "make": str(make),
            "model": str(model),
            "year": int(year) if year else 0,
            "component": str(comp),
            "vehicle_category": str(vcat),
            "crash": str(crash),
            "fire": str(fire)
        })
        
        if len(ids) >= batch_size or i == len(all_rows) - 1:
            collection.upsert(ids=ids, documents=docs, metadatas=metadatas)
            ids, docs, metadatas = [], [], []
            if (i + 1) % 2500 == 0 or i == len(all_rows) - 1:
                print(f"Indexed {i + 1} / {len(all_rows)} complaint narratives...")
                
    print(f"Vector indexing complete! Total documents in collection: {collection.count()}")
    return collection

def search_complaints(query, top_k=5, vehicle_category=None):
    """
    Retrieves top_k nearest complaint narratives for a query.
    """
    client = get_chroma_client()
    collection = client.get_collection(name="nhtsa_complaints")
    
    where_filter = None
    if vehicle_category:
        where_filter = {"vehicle_category": vehicle_category}
        
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter
    )
    return results

if __name__ == "__main__":
    coll = index_complaints(max_motorcycles=6000, max_cars=8000)
    print("Testing query retrieval on BMW R1200GS rear brake:")
    res = search_complaints("BMW R1200GS rear brake pedal loss pressure spongy", top_k=3, vehicle_category="motorcycle")
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        print(f"[{meta['cmplid']}] {meta['make']} {meta['model']} ({meta['year']}): {doc[:120]}...")
