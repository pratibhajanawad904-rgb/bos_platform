import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
ADMIN_PASSWORD = "Pratii@2004"
# Enable CORS so your Vercel frontend can talk to Render safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "bos_platform.db")

# 1. Comprehensive Timeline Engine Mapping (Derived directly from pages 1 & 2)
def generate_agronomy_rules(crop: str, lang: str, sowing_date_str: str) -> str:
    c_key = crop.lower().strip()
    l_key = lang.lower().strip()
    
    if c_key not in ["sugarcane"]:
        c_key = "sugarcane"
    if l_key not in ["en", "mr", "kn", "te"]:
        l_key = "en"
        
    try:
        sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        days_passed = (today - sowing_date).days
        if days_passed < 0:
            days_passed = 0
    except Exception:
        days_passed = 0

    # Dynamic lookup based on Days After Planting (DAP) thresholds
    if days_passed < 3:
        stage, action, obs = (
            "Planting",
            "Apply Basal fertilizer mix (N:P:K + O-Max) in furrows. Treat setts/buds with Carbendazim + Imidacloprid for 15 mins. Plant at 5x2 ft spacing.",
            "Check that furrow depth is uniform between 9 to 12 inches."
        )
    elif days_passed < 20:
        stage, action, obs = (
            "Pre-emergence",
            "Spray Atrazine 50% WP at 1 kg/acre across fields using a flat-fan nozzle. Ensure the soil has optimal moisture before spraying.",
            "Monitor for soil crusting or cracking which might block bud emergence."
        )
    elif days_passed < 30:
        stage, action, obs = (
            "Germination",
            "Bio-Bramha Tillering Dose via Drench or drip system. Maintain light, frequent drip irrigation cycles regularly.",
            "Watch for initial green shoots poking through the soil across rows."
        )
    elif days_passed < 45:
        stage, action, obs = (
            "Establishment",
            "Execute root zone drenching/drip with Humic Acid (500ml) + 19:19:19 (5kg) per acre. Manually fill gaps using healthy nursery seedlings.",
            "Critical: Check for fields with less than 85% germination uniformity. Fill gaps immediately."
        )
    elif days_passed < 60:
        stage, action, obs = (
            "Tillering Start",
            "Run mini-tractor/cultivator for mechanical weed clearance and soil aeration. Apply first top dress of Nitrogen (40 kg/acre) via drip/side-band.",
            "Look for early side-shoots (tillers) emerging from the base of the mother plant."
        )
    elif days_passed < 75:
        stage, action, obs = (
            "Active Tillering",
            "Spray 1% Urea + 1% Magnesium Sulfate + 0.5% Micronutrient mix. Release Trichogramma chilonis parasite cards at 2.5 cc/acre spray for early shoot borer.",
            "Check for dead hearts (withered central leaf whorl), indicating Early Shoot Borer attack. Count tillers on random clumps (target 4-5 robust tillers)."
        )
    elif days_passed < 90:
        stage, action, obs = (
            "Peak Tillering",
            "Inject second top dress of Nitrogen (40 kg) + Potassium (20 kg) + Humate per acre via drip. Maintain uniform soil moisture to support new tiller buds.",
            "Observe soil structure around the base. Ensure soil is loose and loose earth covers the early roots."
        )
    elif days_passed < 100:
        stage, action, obs = (
            "Tillering Phase",
            "Perform light earthing-up using a ridge-cultivator. If broad-leaf weeds or nut grass are visible, spray Halosulfuron-methyl at 36g/acre.",
            "Identify and monitor the primary stems. Late, thin, or thread-like tillers must be suppressed."
        )
    elif days_passed < 120:
        stage, action, obs = (
            "Tiller Selection",
            "Inject Bio-Bramha Biostimulant via drip system/Drenching to transition the crop into accelerated cell division.",
            "Confirm that the target density of 1 strong cane per square foot is clear of parasitic tillers."
        )
    elif days_passed < 150:
        stage, action, obs = (
            "Grand Growth",
            "Perform Heavy Earthing Up to bury weak tillers and stabilize primary stems. Apply 20 kg Sulphate of Potash per acre via drip.",
            "Inspect the lower leaf sheaths for early presence of scales or mealybugs. Check internode spacing."
        )
    elif days_passed < 180:
        stage, action, obs = (
            "Internode Elongation",
            "Spray Orthosilicic Acid (Silicon) at 1ml/L + Boron (20%) at 1g/L to strengthen cane walls and prepare for heavy weight accumulation.",
            "Check for any signs of leaning or lodging after strong winds or heavy watering."
        )
    elif days_passed < 210:
        stage, action, obs = (
            "Cane Weight Max",
            "Execute first de-trashing (remove dry, dead lower leaves) and tie adjacent cane rows together (propping) to prevent tipping.",
            "Observe the rind color deepening and check the thickness of the cane diameter."
        )
    elif days_passed < 300:
        stage, action, obs = (
            "Maturation Start",
            "Spray second round of Silicon + Boron. Reduce water volume slightly via drip, switching to a maintenance irrigation volume.",
            "Monitor brix values using a hand-refractometer."
        )
    else:
        stage, action, obs = (
            "Maturity/Harvest",
            "Stop irrigation entirely 15 days before the scheduled harvest date to force maximum sugar synthesis and concentration.",
            "Target brix reading for harvest: 18-20%."
        )

    # Translation dictionary mapping
    translations = {
        "en": f"Day {days_passed} — [{stage} Stage]\n\n🔔 ACTION REQUIRED:\n{action}\n\n👁️ FIELD OBSERVATION CHECKLIST:\n{obs}",
        "kn": f"ದಿನ {days_passed} — [{stage} ಹಂತ]\n\n🔔 ಅಗತ್ಯ ಕ್ರಮಗಳು:\n{action}\n\n👁️ ಕ್ಷೇತ್ರ ಪರಿಶೀಲನೆ ಪಟ್ಟಿ:\n{obs}",
        "te": f"రోజు {days_passed} — [{stage} దశ]\n\n🔔 చేయవలసిన చర్య:\n{action}\n\n👁️ పంట పరిశీలన జాబితా:\n{obs}"
    }
    
    return translations[l_key]

# 2. Database Initialization
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

# 3. Model Definition
class PlotForm(BaseModel):
    farmer_name: str
    phone_number: str
    crop: str
    acreage: int
    date: str
    lang: str = "en"

# 4. GET Endpoint
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

# 5. POST Endpoint
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