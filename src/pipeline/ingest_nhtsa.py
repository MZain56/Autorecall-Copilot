import os
import zipfile
import duckdb
import time

base_dir = r'c:\Users\Mohammed Zain\Capstone Project'
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(proc_dir, exist_ok=True)

db_path = os.path.join(proc_dir, 'autorecall.duckdb')

print("=== NHTSA Data Ingestion Pipeline ===")
print(f"Connecting to DuckDB at: {db_path}")
con = duckdb.connect(db_path)

# 1. Extract files
print("\n--- Step 1: Extracting archives ---")
cmpl_zip = os.path.join(raw_dir, 'FLAT_CMPL.zip')
rcl_zip = os.path.join(raw_dir, 'FLAT_RCL_POST_2010.zip')

with zipfile.ZipFile(rcl_zip) as z:
    for f in z.namelist():
        if f.endswith('.txt'):
            z.extract(f, raw_dir)
            rcl_txt = os.path.join(raw_dir, f)
            print(f"Extracted recalls text: {rcl_txt} ({os.path.getsize(rcl_txt)/(1024*1024):.1f} MB)")

with zipfile.ZipFile(cmpl_zip) as z:
    for f in z.namelist():
        if f.endswith('.txt'):
            z.extract(f, raw_dir)
            cmpl_txt = os.path.join(raw_dir, f)
            print(f"Extracted complaints text: {cmpl_txt} ({os.path.getsize(cmpl_txt)/(1024*1024):.1f} MB)")

# 2. Ingest Recalls
print("\n--- Step 2: Ingesting Recalls into DuckDB ---")
rcl_columns = [
    "RECORD_ID", "CAMPNO", "MAKETXT", "MODELTXT", "YEARTXT", "MFGCAMPNO",
    "COMPNAME", "MFGNAME", "BGMAN", "ENDMAN", "RCLTYPECD", "POTAFF",
    "ODATE", "INFLUENCED_BY", "MFGTXT", "RCDATE", "DATEA", "RPNO",
    "FMVSS", "DESC_DEFECT", "CONEQUENCE_DEFECT", "CORRECTIVE_ACTION",
    "NOTES", "RCL_CMPT_ID", "MFR_COMP_NAME", "MFR_COMP_DESC", "MFR_COMP_PTNO",
    "DO_NOT_DRIVE", "PARK_OUTSIDE"
]

con.execute("DROP TABLE IF EXISTS raw_recalls;")
con.execute(f"""
    CREATE TABLE raw_recalls AS 
    SELECT * FROM read_csv('{rcl_txt.replace("\\", "/")}', 
        delim='\\t', 
        header=False, 
        names={rcl_columns},
        all_varchar=True,
        ignore_errors=True
    );
""")
rcl_total = con.execute("SELECT count(*) FROM raw_recalls;").fetchone()[0]
print(f"Total raw recall records ingested: {rcl_total:,}")

# Filter Recalls 2015-2025
con.execute("DROP TABLE IF EXISTS recalls_clean;")
con.execute("""
    CREATE TABLE recalls_clean AS
    SELECT 
        RECORD_ID, CAMPNO, MAKETXT, MODELTXT, YEARTXT, COMPNAME, MFGNAME,
        RCDATE, DATEA, DESC_DEFECT, CONEQUENCE_DEFECT, CORRECTIVE_ACTION,
        CASE 
            WHEN upper(MAKETXT) IN ('HARLEY-DAVIDSON', 'HARLEY DAVIDSON', 'DUCATI', 'KTM', 'TRIUMPH', 'INDIAN MOTORCYCLE', 'HUSQVARNA', 'APRILIA', 'MOTO GUZZI', 'ROYAL ENFIELD')
                 OR (upper(MAKETXT) = 'BMW' AND (upper(MODELTXT) LIKE 'R%' OR upper(MODELTXT) LIKE 'K%' OR upper(MODELTXT) LIKE 'F%' OR upper(MODELTXT) LIKE 'S1000%' OR upper(MODELTXT) LIKE 'G310%'))
                 OR (upper(MAKETXT) = 'HONDA' AND (upper(MODELTXT) LIKE '%CBR%' OR upper(MODELTXT) LIKE '%CRF%' OR upper(MODELTXT) LIKE '%GOLDWING%' OR upper(MODELTXT) LIKE '%REBEL%' OR upper(MODELTXT) LIKE '%SHADOW%' OR upper(MODELTXT) LIKE '%AFRICA TWIN%'))
                 OR (upper(MAKETXT) IN ('YAMAHA', 'KAWASAKI', 'SUZUKI') AND upper(MODELTXT) NOT LIKE '%AUTO%')
            THEN 'motorcycle'
            ELSE 'passenger_car'
        END AS vehicle_category
    FROM raw_recalls
    WHERE try_cast(substr(coalesce(RCDATE, DATEA), 1, 4) AS INTEGER) BETWEEN 2015 AND 2025;
""")
rcl_window = con.execute("SELECT count(*) FROM recalls_clean;").fetchone()[0]
rcl_moto = con.execute("SELECT count(*) FROM recalls_clean WHERE vehicle_category='motorcycle';").fetchone()[0]
rcl_car = con.execute("SELECT count(*) FROM recalls_clean WHERE vehicle_category='passenger_car';").fetchone()[0]
print(f"Recalls 2015-2025: {rcl_window:,} (Cars: {rcl_car:,}, Motorcycles: {rcl_moto:,})")

# 3. Ingest Complaints
print("\n--- Step 3: Ingesting Complaints into DuckDB ---")
cmpl_columns = [
    "CMPLID", "ODINO", "MFR_NAME", "MAKETXT", "MODELTXT", "YEARTXT", "CRASH",
    "FAILDATE", "FIRE", "INJURED", "DEATHS", "COMPDESC", "CITY", "STATE",
    "VIN", "DATEA", "LDATE", "MILES", "OCCURENCES", "CDESCR", "CMPL_TYPE",
    "POLICE_RPT_YN", "PURCH_DT", "ORIG_OWNER_YN", "ANTI_BRAKES_YN", "CRUISE_CONT_YN",
    "NUM_CYLS", "DRIVE_TRAIN", "FUEL_SYS", "FUEL_TYPE", "TRANS_TYPE", "VEH_SPEED",
    "DOT", "TIRE_SIZE", "LOC_OF_TIRE", "TIRE_FAIL_TYPE", "ORIG_EQUIP_YN", "MANUF_DT",
    "SEAT_TYPE", "RESTRAINT_TYPE", "DEALER_NAME", "DEALER_TEL", "DEALER_CITY",
    "DEALER_STATE", "DEALER_ZIP", "PROD_TYPE", "REPAIRED_YN", "MEDICAL_ATTN",
    "VEHICLES_TOWED_YN", "STATE_OF_INCIDENT", "VEHICLE_OPERATOR"
]

con.execute("DROP TABLE IF EXISTS raw_complaints;")
con.execute(f"""
    CREATE TABLE raw_complaints AS 
    SELECT * FROM read_csv('{cmpl_txt.replace("\\", "/")}', 
        delim='\\t', 
        header=False, 
        names={cmpl_columns},
        all_varchar=True,
        ignore_errors=True
    );
""")
cmpl_total = con.execute("SELECT count(*) FROM raw_complaints;").fetchone()[0]
print(f"Total raw complaint records ingested: {cmpl_total:,}")

# Filter Complaints 2015-2025
con.execute("DROP TABLE IF EXISTS complaints_clean;")
con.execute("""
    CREATE TABLE complaints_clean AS
    SELECT 
        CMPLID, ODINO, MFR_NAME, upper(trim(MAKETXT)) AS MAKETXT, upper(trim(MODELTXT)) AS MODELTXT, 
        YEARTXT, CRASH, FAILDATE, FIRE, INJURED, DEATHS, COMPDESC, CITY, STATE, VIN, 
        DATEA, LDATE, MILES, CDESCR, PROD_TYPE,
        CASE 
            WHEN upper(trim(MAKETXT)) IN ('HARLEY-DAVIDSON', 'HARLEY DAVIDSON', 'DUCATI', 'KTM', 'TRIUMPH', 'INDIAN MOTORCYCLE', 'HUSQVARNA', 'APRILIA', 'MOTO GUZZI', 'ROYAL ENFIELD')
                 OR (upper(trim(MAKETXT)) = 'BMW' AND (upper(MODELTXT) LIKE 'R%' OR upper(MODELTXT) LIKE 'K%' OR upper(MODELTXT) LIKE 'F%' OR upper(MODELTXT) LIKE 'S1000%' OR upper(MODELTXT) LIKE 'G310%'))
                 OR (upper(trim(MAKETXT)) = 'HONDA' AND (upper(MODELTXT) LIKE '%CBR%' OR upper(MODELTXT) LIKE '%CRF%' OR upper(MODELTXT) LIKE '%GOLDWING%' OR upper(MODELTXT) LIKE '%REBEL%' OR upper(MODELTXT) LIKE '%SHADOW%' OR upper(MODELTXT) LIKE '%AFRICA TWIN%' OR upper(MODELTXT) LIKE 'CB%'))
                 OR (upper(trim(MAKETXT)) IN ('YAMAHA', 'KAWASAKI', 'SUZUKI') AND upper(MODELTXT) NOT LIKE '%AUTO%')
            THEN 'motorcycle'
            ELSE 'passenger_car'
        END AS vehicle_category
    FROM raw_complaints
    WHERE try_cast(substr(coalesce(DATEA, LDATE), 1, 4) AS INTEGER) BETWEEN 2015 AND 2025
      AND (PROD_TYPE = 'V' OR PROD_TYPE IS NULL);
""")
cmpl_window = con.execute("SELECT count(*) FROM complaints_clean;").fetchone()[0]
cmpl_moto = con.execute("SELECT count(*) FROM complaints_clean WHERE vehicle_category='motorcycle';").fetchone()[0]
cmpl_car = con.execute("SELECT count(*) FROM complaints_clean WHERE vehicle_category='passenger_car';").fetchone()[0]
print(f"Complaints 2015-2025: {cmpl_window:,} (Cars: {cmpl_car:,}, Motorcycles: {cmpl_moto:,})")

# Motorcycle OEM Breakdown
print("\n--- Top Motorcycle OEMs in Complaints ---")
moto_oems = con.execute("""
    SELECT MAKETXT, count(*) as count 
    FROM complaints_clean 
    WHERE vehicle_category='motorcycle' 
    GROUP BY MAKETXT 
    ORDER BY count DESC 
    LIMIT 10;
""").fetchall()
for make, cnt in moto_oems:
    print(f"  {make}: {cnt:,}")

# Data Quality Audits
missing_vin = con.execute("SELECT count(*) FROM complaints_clean WHERE VIN IS NULL OR trim(VIN) = '';").fetchone()[0]
vin_pct = (missing_vin / cmpl_window) * 100
crash_count = con.execute("SELECT count(*) FROM complaints_clean WHERE CRASH = 'Y';").fetchone()[0]
crash_moto = con.execute("SELECT count(*) FROM complaints_clean WHERE vehicle_category='motorcycle' AND CRASH = 'Y';").fetchone()[0]

print(f"\nMissing VINs in complaints: {missing_vin:,} ({vin_pct:.1f}%)")
print(f"Total crash incidents: {crash_count:,} (Motorcycle crashes: {crash_moto:,}, {crash_moto/cmpl_moto*100:.1f}%)")

con.close()
print("\n=== Ingestion Completed Successfully! ===")

