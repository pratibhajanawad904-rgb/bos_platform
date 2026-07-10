import os
import sqlite3

# This forces the database file to be created right inside the frontend folder!
DB_PATH = os.path.join(os.path.dirname(__file__), "bos_platform.db")

print(f"Connecting directly to database at: {DB_PATH}\n")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS plots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_name TEXT,
        phone TEXT,
        crop_type TEXT,
        sowing_date TEXT,
        acreage REAL,
        selected_lang TEXT,
        status TEXT DEFAULT 'Synced with Local DB'
    )
""")

test_farmer = "Anandrao Patil"
test_phone = "9876543210"
test_crop = "Sugarcane"
test_date = "2026-06-22"
test_acreage = 4.5
test_lang = "mr"

try:
    cursor.execute("""
        INSERT INTO plots (owner_name, phone, crop_type, sowing_date, acreage, selected_lang)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (test_farmer, test_phone, test_crop, test_date, test_acreage, test_lang))
    
    conn.commit()
    print("✅ Success! Data written perfectly to the database table row.")
except Exception as e:
    print(f"❌ Error writing data: {str(e)}")

print("\n--- Current Saved Database Records ---")
cursor.execute("SELECT * FROM plots")
rows = cursor.fetchall()

if not rows:
    print("Database is empty.")
else:
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Crop: {row[3]} | Date: {row[4]} | Acres: {row[5]}")

conn.close()