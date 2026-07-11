import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS so your Vercel frontend can talk to Render safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "bos_platform.db")

# 1. Base Agronomy Rules Matrix
advisory_matrix = {
    "sugarcane": {
        "en": "Day {days} — [Early Root Zone Drenching]: Execute root zone drenching loop using Humic Acid (500ml/acre) to accelerate root branching.\n\nPROACTIVE CAPA: Maintain inline drip irrigation cycles.\n\nCORRECTIVE CAPA: Watch for early uniform green shoots.",
        "kn": "ದಿನ {days} — [ಸಸಿ ರಕ್ಷಣೆ]: ಸಮತೋಲಿತ ನೀರಾವರಿ ನಿರ್ವಹಣೆ ಮತ್ತು ಪೋಷಕಾಂಶಗಳ ಪೂರೈಕೆ.",
        "te": "రోజు {days} — [మొలకల రక్షణ]: సమతుల్య నీటి యాజమాన్యం మరియు పోషకాల సరఫరా."
    }
}

# 2. Dynamic Advisory Calculation Function
def generate_agronomy_rules(crop: str, lang: str, sowing_date_str: str) -> str:
    c_key = crop.lower().strip()
    l_key = lang.lower().strip()
    
    if c_key not in advisory_matrix:
        c_key = "sugarcane"
    if l_key not in ["en", "mr", "kn", "te"]:
        l_key = "en"
        
    try:
        # Calculate exactly how many days have passed since sowing
        sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        days_passed = (today - sowing_date).days
        
        # Prevent 0 or negative values if the date is in the future/today
        if days_passed < 1:
            days_passed = 1
    except Exception:
        days_passed = 9 # Fallback day default if date string parsing breaks
        
    base_template = advisory_matrix[c_key][l_key]
    
    # Inject the actual day counter into the matrix string template dynamically
    return base_template.format(days=days_passed)

# 3. Database Initializer (Builds table with phone_number securely)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            crop TEXT NOT NULL,
            acreage INTEGER NOT NULL,
            sowing_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 4. Pydantic Request Models
class PlotForm(BaseModel):
    farmer_name: str
    phone_number: str
    crop: str
    acreage: int
    date: str
    lang: str = "en"

# 5. GET API: Retrieve all plots with calculated ages
@app.get("/api/plots")
def get_plots():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT owner_name, phone_number, crop, acreage, sowing_date FROM plots")
        rows = cursor.fetchall()
        
        return [
            {
                "owner_name": r[0],
                "phone": r[1],
                "crop": r[2],
                "acreage": r[3],
                "date": r[4],
                "advisory": generate_agronomy_rules(r[2], "en", r[4])
            }
            for r in rows
        ]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# 6. POST API: Save new layout records
@app.post("/api/plots")
def register_plot(form: PlotForm):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO plots (owner_name, phone_number, crop, acreage, sowing_date) VALUES (?, ?, ?, ?, ?)",
            (form.farmer_name, form.phone_number, form.crop, form.acreage, form.date)
        )
        conn.commit()
        return {"message": "Plot registration successful."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()