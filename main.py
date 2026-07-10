import sqlite3
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlotForm(BaseModel):
    farmer_name: str
    phone_number: str
    crop: str
    date: str
    acreage: float
    lang: str

class ChatForm(BaseModel):
    text_payload: str
    sender_role: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bos_platform.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT,
            phone_number TEXT,
            crop TEXT,
            date TEXT,
            acreage REAL,
            advisory TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_payload TEXT,
            sender_role TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# COMPREHENSIVE MULTI-LINGUAL ADVISORY ENGINE
advisory_matrix = {
    "sugarcane": {
        "en": "Day 9 — [Early Root Zone Drenching]: Execute root zone drenching loop using Humic Acid (500ml/acre) to accelerate root branching.\n\nPROACTIVE CAPA: Maintain inline drip irrigation cycles.\n\nCORRECTIVE CAPA: Watch for early uniform green shoots.",
        "mr": "दिवस ९ — [सुरुवातीची मूळ झोन ड्रेंचिंग]: मुळांच्या वाढीसाठी ह्युमिक ऍसिड (५०० मिली/एकर) वापरून ड्रेंचिंग करा.\n\nखबरदारी: ठिबक सिंचन चक्र नियमित ठेवा.\n\nदुरुस्ती उपाय: पिकाच्या ओळींमध्ये सुरुवातीच्या हिरव्या कोंबांवर बारीक लक्ष ठेवा.",
        "kn": "ದಿನ 9 — [ಆರಂಭಿಕ ಬೇರು ವಲಯ ಡ್ರೆಂಚಿಂಗ್]: ಬೇರುಗಳ ಬೆಳವಣಿಗೆಯನ್ನು ವೇಗಗೊಳಿಸಲು ಹ್ಯೂಮಿಕ್ ಆಸಿಡ್ (500ml/ಎಕರೆ) ಬಳಸಿ ಡ್ರೆಂಚಿಂಗ್ ಮಾಡಿ.\n\nಮುನ್ನೆಚ್ಚರಿಕೆ: ಹನಿ ನೀರಾವರಿ ಚಕ್ರಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ನಿರ್ವಹಿಸಿ.\n\nದುರಸ್ತಿ ಕ್ರಮ: ಸಾಲುಗಳಲ್ಲಿ ಆರಂಭಿಕ ಹಸಿರು ಚಿಗುರುಗಳನ್ನು ಗಮನಿಸಿ.",
        "te": "రోజు 9 — [ప్రారంభ రూట్ జోన్ డ్రెంచింగ్]: వేర్ల పెరుగుదలను వేగవంతం ಮಾಡಲು హ్యూమిక్ యాసిಡ್ (500ml/ఎకరం) ఉపయోగించి రూట్ జోన్ డ్రెంచింగ్ చేయండి.\n\nముందుజాగ్రత్త: డ్రిప్ ఇరిగేషన్ సైకిల్స్ క్రమం తప్పకుండా నిర్వహించండి.\n\nనివారణ చర్య: వరుసలలో ప్రారంభ పచ్చని మొలకలను గమనించండి."
    },
    "cotton": {
        "en": "Day 5 — [Seedling Protection]: Ensure balanced nitrogen application. Check soil conditions for optimal moisture retention.\n\nPROACTIVE CAPA: Keep drainage channels clear.\n\nCORRECTIVE CAPA: Spray organic biological shields if pests emerge.",
        "mr": "दिवस ५ — [रोप संरक्षण]: संतुलित नत्र खत वापरल्याची खात्री करा. जमिनीतील ओलावा तपासा.\n\nखबरदारी: पाण्याचा निचरा होणारे चर मोकळे ठेवा.\n\nदुरुस्ती उपाय: कीड दिसून आल्यास सेंद्रिय जैविक फवारणी करा.",
        "kn": "ದಿನ 5 — [ಸಸಿ ರಕ್ಷಣೆ]: ಸಮತೋಲಿತ ಸಾರಜನಕ ಅನ್ವಯವನ್ನು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. ಮಣ್ಣಿನ ತೇವಾಂಶವನ್ನು ಪರೀಕ್ಷಿಸಿ.\n\nಮುನ್ನೆಚ್ಚರಿಕೆ: ಒಳಚರಂಡಿ ಕಾಲುವೆಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.\n\nದುರಸ್ತಿ ಕ್ರಮ: ಕೀಟಗಳು ಕಂಡುಬಂದಲ್ಲಿ ಸಾವಯವ ಜೈವಿಕ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಿ.",
        "te": "రోజు 5 — [మొలకల రక్షణ]: సమతుల్య నత్రజని వినియోగాన్ని నిర్ధారించుకోండి. నేల తేమను పరీక్షించండి.\n\nముందుజాగ్రత్త: నీటి పారుదల కాలువలను శుభ್ರంగా ఉంచండి.\n\nనివారణ చర్య: తెగుళ్లు ಕಂಡುಬಂದಲ್ಲಿ సేంద్రీయ బయో-స్ప్రేలను ఉపయోగించండి."
    }
}

def generate_agronomy_rules(crop, lang):
    c_key = crop.lower().strip()
    l_key = lang.lower().strip()
    
    if c_key not in advisory_matrix:
        c_key = "sugarcane"
    if l_key not in ["en", "mr", "kn", "te"]:
        l_key = "en"
        
    return advisory_matrix[c_key][l_key]

@app.get("/api/plots")
async def get_plots():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT owner_name, phone_number, crop, date, acreage, advisory FROM plots ORDER BY id DESC")
        rows = cursor.fetchall()
        return [{"owner_name": r[0], "phone": r[1], "crop": r[2], "date": r[3], "acreage": r[4], "advisory": r[5]} for r in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.post("/api/plots")
async def register_plot(form: PlotForm):
    clean_phone = form.phone_number.strip().replace("+91", "").strip()
    
    if not clean_phone.isdigit() or len(clean_phone) != 10:
        raise HTTPException(status_code=400, detail="Invalid mobile length.")
    if clean_phone in ["1234567890", "0000000000", "9999999999"]:
        raise HTTPException(status_code=400, detail="Prohibited sequence blocked.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id FROM plots 
            WHERE phone_number = ? AND crop = ? AND date = ? AND acreage = ?
        """, (form.phone_number.strip(), form.crop, form.date, form.acreage))
        
        duplicate = cursor.fetchone()
        if duplicate:
            return {"status": "ignored", "message": "Duplicate registration skipped."}
            
        advisory_text = generate_agronomy_rules(form.crop, form.lang)
        
        cursor.execute("""
            INSERT INTO plots (owner_name, phone_number, crop, date, acreage, advisory)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (form.farmer_name.strip(), form.phone_number.strip(), form.crop, form.date, form.acreage, advisory_text))
        
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/api/chat")
async def get_chats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT text_payload, sender_role FROM chats ORDER BY id ASC")
        rows = cursor.fetchall()
        return [{"text_payload": r[0], "sender_role": r[1]} for r in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.post("/api/chat")
async def post_chat(form: ChatForm):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO chats (text_payload, sender_role) VALUES (?, ?)", (form.text_payload, form.sender_role))
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()