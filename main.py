import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI
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

DB_PATH = os.path.join(os.path.dirname(__file__), "bos_platform.db")
ADMIN_PASSWORD = "Pratii@2004"

def generate_agronomy_rules(crop: str, lang: str, sowing_date_str: str) -> str:
    c_key = crop.lower().strip()
    l_key = lang.lower().strip()
    
    if l_key == "kan": l_key = "kn"
    if l_key == "telgu": l_key = "te"
    
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

    if days_passed < 3:
        stage = {"en": "Planting", "mr": "लागवड", "kn": "ನಾಟಿ", "te": "నాటడం"}
        action = {
            "en": "Apply Basal fertilizer mix (N:P:K + O-Max) in furrows. Treat setts/buds with Carbendazim + Imidacloprid for 15 mins. Plant at 5x2 ft spacing.",
            "mr": "सऱ्यांमध्ये बेसल खत मिश्रण (N:P:K + O-Max) टाका. बेणे १५ मिनिटे कार्बेन्डाझिम + इमिडाक्लोप्रिड द्रावणात बुडवा. ५x२ फूट अंतरावर लागवड करा.",
            "kn": "ಸಾಲುಗಳಲ್ಲಿ ಬೇಸಲ್ ಗೊಬ್ಬರ ಮಿಶ್ರಣವನ್ನು (N:P:K + O-Max) ಹಾಕಿ. ಕಬ್ಬಿನ ಜಲ್ಲೆಗಳನ್ನು 15 ನಿಮಿಷ ಕಾರ್ಬೆಂಡಾಜಿಮ್ + ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್‌ನಲ್ಲಿ ಉಪಚರಿಸಿ. 5x2 ಅಡಿ ಅಂತರದಲ್ಲಿ ನಾಟಿ ಮಾಡಿ.",
            "te": "సాలులలో బేసల్ ఎరువుల మిశ్రమాన్ని (N:P:K + O-Max) వేయండి. విత్తన ముక్కలను 15 నిమిషాల పాటు కార్బెండజిమ్ + ఇమిడాక్లోప్రిడ్‌తో శుద్ధి చేయండి. 5&times;2 అడుగుల దూరంలో నాటండి."
        }
        obs = {
            "en": "Check that furrow depth is uniform between 9 to 12 inches.",
            "mr": "सऱ्यांची खोली ९ ते १२ इंच समान असल्याची खात्री करा.",
            "kn": "ಸಾಲಿನ ಆಳವು 9 ರಿಂದ 12 ಇಂಚುಗಳಷ್ಟು ಏಕರೂಪವಾಗಿರುವುದನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "te": "సాలు లోతు 9 నుండి 12 అంగుళాల వరకు ఒకేలా ఉందో లేど తనిఖీ చేయండి."
        }
    elif days_passed < 20:
        stage = {"en": "Pre-emergence", "mr": "उगवणपूर्व अवस्था", "kn": "ಮೊಳಕೆ ಪೂರ್ವ ಹಂತ", "te": "మొలకల ముందు దశ"}
        action = {
            "en": "Spray Atrazine 50% WP at 1 kg/acre across fields using a flat-fan nozzle. Ensure the soil has optimal moisture before spraying.",
            "mr": "फ्लॅट-फॅन नोजल वापरून शेतात १ किलो/एकर या दराने ॲट्राझिन ५०% डब्ल्यूपी फवारा. फवारणीपूर्वी जमिनीत योग्य ओलावा असल्याची खात्री करा.",
            "kn": "ಫ್ಲಾಟ್-ಫ್ಯಾನ್ ನಾಝಲ್ ಬಳಸಿ ಎಕರೆಗೆ 1 ಕೆಜಿ ಅಟ್ರಾಜಿನ್ 50% WP ಸಿಂಪಡಿಸಿ. ಸಿಂಪಡಿಸುವ ಮೊದಲು ಮಣ್ಣಿನಲ್ಲಿ ಉತ್ತಮ ತೇವಾಂಶವಿರುವುದನ್ನು khachitapadisikolli.",
            "te": "ఫ్లాట్-యాన్ నాజిల్ ఉపయోగించి ఎకరాకు 1 కిలో అట్రాజిన్ 50% WP పిచికారీ చేయండి. పిచికారీ చేయడానికి ముందు నేలలో తగినంత తేమ ఉండేలా చూసుకోండి."
        }
        obs = {
            "en": "Monitor for soil crusting or cracking which might block bud emergence.",
            "mr": "जमिनीला पापुद्रे येणे किंवा तडे जाणे यावर लक्ष ठेवा, ज्यामुळे कोंब उगवण्यास अडथळा येऊ शकतो.",
            "kn": "ಮಣ್ಣು ಗಟ್ಟಿಯಾಗುವುದು ಅಥವಾ ಬಿರುಕು ಬಿಡುವುದನ್ನು ಗಮನಿಸಿ, ಇದು ಮೊಳಕೆ ಬರುವುದನ್ನು ತಡೆಯಬಹುದು.",
            "te": "నేల గట్టిపడటం లేదా పగుళ్లు రావడం గమనించండి, ఇది మొలకలు రాకుండా నిరోధించవచ్చు."
        }
    elif days_passed < 30:
        stage = {"en": "Germination", "mr": "उगवण अवस्था", "kn": "ಮೊಳಕೆಯೊಡೆಯುವಿಕೆ", "te": "మొలకెత్తడం"}
        action = {
            "en": "Bio-Bramha Tillering Dose via Drench or drip system. Maintain light, frequent drip irrigation cycles regularly.",
            "mr": "ड्रेंचिंग किंवा ठिबक सिंचनाद्वारे बायो-ब्रह्मा टिलरिंग डोस द्या. नियमितपणे हलके व वारंवार ठिबक सिंचन चक्र चालू ठेवा.",
            "kn": "ಡ್ರಿಪ್ ಅಥವಾ ಡ್ರೆಂಚಿಂಗ್ ಮೂಲಕ ಬಯೋ-ಬ್ರಹ್ಮ ಟಿಲ್ಲರಿಂಗ್ ಡೋಸ್ ನೀಡಿ. ನಿಯಮಿತವಾಗಿ ಲಘು ನೀರಾವರಿ ನಿರ್ವಹಣೆ ಮಾಡಿ.",
            "te": "డ్రిప్ లేదా డ్రెంచింగ్ ద్వారా బయో-బ్రహ్మ పిలకల డోస్ అందించండి. క్రమం తప్పకుండా తేలికపాటి నీటి సరఫరా చేయండి."
        }
        obs = {
            "en": "Watch for initial green shoots poking through the soil across rows.",
            "mr": "सऱ्यांमध्ये जमिनीतून बाहेर येणारे सुरुवातीचे हिरवे कोंब पहा.",
            "kn": "ಸಾಲುಗಳಲ್ಲಿ ಮಣ್ಣಿನಿಂದ ಹೊರಬರುತ್ತಿರುವ ಆರಂಭಿಕ ಹಸಿರು ಚಿಗುರುಗಳನ್ನು ಗಮನಿಸಿ.",
            "te": "సాలులలో నేలపైకి వస్తున్న ప్రారంభ పచ్చని మొలకలను గమనించండి."
        }
    elif days_passed < 45:
        stage = {"en": "Establishment", "mr": "स्थिरीकरण अवस्था", "kn": "ಸ್ಥಾಪನೆ ಹಂತ", "te": "స్థిరపడే దశ"}
        action = {
            "en": "Execute root zone drenching/drip with Humic Acid (500ml) + 19:19:19 (5kg) per acre. Manually fill gaps using healthy nursery seedlings.",
            "mr": "प्रति एकर ह्युमिक ॲसिड (५०० मिली) + १९:१९:१९ (५ किलो) सह मूळ क्षेत्रात आळवणी/ठिबक करा. नर्सरीतील निरोगी रोपे वापरून नांग्या भरा.",
            "kn": "ಎಕರೆಗೆ ಹ್ಯೂಮಿಕ್ ಆಸಿಡ್ (500ml) + 19:19:19 (5kg) ನೊಂದಿಗೆ ಬೇರಿನ ವಲಯಕ್ಕೆ ಡ್ರೆಂಚಿಂಗ್ ಮಾಡಿ. ನರ್ಸರಿ ಸಸಿಗಳನ್ನು ಬಳಸಿ ಖಾಲಿ ಜಾಗಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ.",
            "te": "ఎకరాకు హ్యూమిక్ యాసిడ్ (500ml) + 19:19:19 (5kg) తో వేర్ల వద్ద డ్రెంచింగ్ చేయండి. నర్సరీ మొక్కలతో ఖాళీలను పూరించండి."
        }
        obs = {
            "en": "Critical: Check for fields with less than 85% germination uniformity. Fill gaps immediately.",
            "mr": "अत्यंत महत्त्वाचे: शेतात ८५% पेक्षा कमी उगवण एकसारखी असल्यास तपासा. त्वरित नांग्या भरा.",
            "kn": "ಬಹಳ ಮುಖ್ಯ: ಶೇ. 85 ಕ್ಕಿಂತ ಕಡಿಮೆ ಏಕರೂಪದ ಮೊಳಕೆ ಇರುವ ಕ್ಷೇತ್ರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. ತಕ್ಷಣ ಗ್ಯಾಪ್ ಫಿಲ್ಲಿಂಗ್ ಮಾಡಿ.",
            "te": "చాలా ముఖ్యం: 85% కంటే తక్కువ మొలకల శాతం ఉన్న పొలాలను తనిఖీ చేయండి. వెంటనే ఖాళీలను పూరించండి."
        }
    elif days_passed < 60:
        stage = {"en": "Tillering Start", "mr": "फुटवे फुटण्यास सुरुवात", "kn": "ಪಿಲಕೆ ಒಡೆಯುವ ಆರಂಭ", "te": "పిలకలు ప్రారంభ దశ"}
        action = {
            "en": "Run mini-tractor/cultivator for mechanical weed clearance and soil aeration. Apply first top dress of Nitrogen (40 kg/acre) via drip/side-band.",
            "mr": "तण काढण्यासाठी आणि माती मोकळी करण्यासाठी मिनी-ट्रॅक्टर/कल्टिव्हेटर चालवा. ठिबकद्वारे नायट्रोजनचा पहिला हप्ता (४० किलो/एकर) द्या.",
            "kn": "ಕಳೆ ತೆಗೆಯಲು ಮತ್ತು ಮಣ್ಣಿನ ವಾತಾಯನಕ್ಕಾಗಿ मಿನಿ ಟ್ರ್ಯಾಕ್ಟರ್ ಚಲಾಯಿಸಿ. ಡ್ರಿಪ್ ಮೂಲಕ ಸಾರಜನಕದ (40 kg/ಎಕರೆ) ಮೊದಲ ಡೋಸ್ ನೀಡಿ.",
            "te": "కలుపు నివారణ మరియు నేల వాతావరణం కోసం మినీ ట్రాక్టర్ నడపండి. డ్రిప్ ద్వారా నైట్రోజన్ (40 kg/ఎకరా) మొదటి డోస్ వేయండి."
        }
        obs = {
            "en": "Look for early side-shoots (tillers) emerging from the base of the mother plant.",
            "mr": "मुख्य पिकाच्या बुंध्यापासून बाहेर येणारे सुरुवातीचे फुटवे (tillers) तपासा.",
            "kn": "ತಾಯಿ ಸಸಿಯ ಬುಡದಿಂದ ಹೊರಬರುತ್ತಿರುವ ಆರಂಭಿಕ ಪಕ್ಕದ ಚಿಗುರುಗಳನ್ನು (ಪಿಲಕೆಗಳನ್ನು) ಗಮನಿಸಿ.",
            "te": "తల్లి మొక్క మొదలు నుండి వస్తున్న ప్రారంభ పక్క పిలకలను గమనించండి."
        }
    elif days_passed < 75:
        stage = {"en": "Active Tillering", "mr": "जोमदार फुटव्यांची अवस्था", "kn": "ಚುರುಕಾದ ಪಿಲಕೆ ಹಂತ", "te": "తీవ్రమైన పిలకల దశ"}
        action = {
            "en": "Spray 1% Urea + 1% Magnesium Sulfate + 0.5% Micronutrient mix. Release Trichogramma chilonis parasite cards at 2.5 cc/acre spray for early shoot borer.",
            "mr": "१% युरिया + १% मॅग्नेशियम सल्फेट + ०.५% सूक्ष्म अन्नद्रव्य मिश्रण फवारा. खोडकिडीसाठी २.५ सीसी/एकर या दराने ट्रायकोगामा चिलोनिस परजीवी कार्ड सोडा.",
            "kn": "1% ಯೂರಿಯಾ + 1% ಮೆಗ್ನೀಸಿಯಮ್ ಸಲ್ಫೇಟ್ + 0.5% ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶ ಮಿಶ್ರಣವನ್ನು ಸಿಂಪಡಿಸಿ. ಕಾಂಡಕೋರಕ ಕೀಟಕ್ಕಾಗಿ ಎಕರೆಗೆ 2.5 cc ಟ್ರೈಕೊಗ್ರಾമാ ಕಾರ್ಡ್‌ಗಳನ್ನು ಬಿಡುగಡೆ ಮಾಡಿ.",
            "te": "1% యూరియా + 1% మెగ్నీషియం సల్ఫేట్ + 0.5% సూక్ష్మపోషకాల మిశ్రమాన్ని పిచికారీ చేయండి. కాండం తొలిచే పురుగు నివారణకు ఎకరాకు 2.5 cc ట్రైకోగ్రామా కార్డ్స్ విడుదల చేయండి."
        }
        obs = {
            "en": "Check for dead hearts (withered central leaf whorl), indicating Early Shoot Borer attack. Count tillers on random clumps (target 4-5 robust tillers).",
            "mr": "खोडकिडीचा प्रादुर्भाव दर्शवणारी सुकलेली पोंगे (dead hearts) तपासा. फुटवे मोजा (लक्ष्य: ४-५ मजबूत फुटवे).",
            "kn": "ಕಾಂಡಕೋರಕ ಬಾಧೆಯನ್ನು ಸೂಚಿಸುವ ಒಣಗಿದ ಸುಳಿಯನ್ನು ಪರಿಶೀಲಿಸಿ. ಯಾದೃಚ್ಛಿಕವಾಗಿ ಪಿಲಕೆಗಳನ್ನು ಎಣಿಸಿ (ಗುри 4-5 ಬಲವಾದ ಪಿಲಕೆಗಳು).",
            "te": "కాండం తొలిచే పురుగు ఉధృతిని సూచించే ఎండిపోయిన సుడిని తనిఖీ చేయండి. పిలకలను లెక్కించండి (లక్ష్యం 4-5 బలమైన పిలకలు)."
        }
    elif days_passed < 90:
        stage = {"en": "Peak Tillering", "mr": "सर्वोच्च फुटव्यांची अवस्था", "kn": "ಗರಿಷ್ಠ ಪಿಲಕೆ ಹಂತ", "te": "గరిష్ట పిలకల దశ"}
        action = {
            "en": "Inject second top dress of Nitrogen (40 kg) + Potassium (20 kg) + Humate per acre via drip. Maintain uniform soil moisture to support new tiller buds.",
            "mr": "ठिबकद्वारे प्रति एकर नायट्रोजन (४० किलो) + पोटॅशियम (२० किलो) + ह्युमेटचा दुसरा हप्ता द्या. नवीन फुटव्यांच्या वाढीसाठी ओलावा टिकवून ठेवा.",
            "kn": "ಡ್ರಿಪ್ ಮೂಲಕ ಎರಡನೇ ಡೋಸ್ ಸಾರಜನಕ (40 kg) + ಪೊಟ್ಯಾಸಿಯಮ್ (20 kg) ನೀಡಿ. ಹೊಸ ಪಿಲಕೆ ಮೊಗ್ಗುಗಳನ್ನು ಬೆಂಬಲಿಸಲು ಮಣ್ಣಿನ ತೇವಾಂಶವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
            "te": "డ్రిప్ ద్వారా రెండవ డోస్ నైట్రోజన్ (40 kg) + పొటాషియం (20 kg) అందించండి. కొత్త పిలకల పెరుగుదలకు నేలలో సమాన తేమను కాపాడండి."
        }
        obs = {
            "en": "Observe soil structure around the base. Ensure soil is loose and loose earth covers the early roots.",
            "mr": "बुंध्याभोवतालच्या मातीची रचना पहा. माती भुसभुशीत असावी आणि सुरुवातीच्या मुळांवर माती पसरलेली असावी.",
            "kn": "ಬುಡದ ಸುತ್ತಲಿನ ಮಣ್ಣಿನ ರಚನೆಯನ್ನು ಗಮನಿಸಿ. ಮಣ್ಣು ಸಡಿಲವಾಗಿದೆಯೇ ಮತ್ತು ಬೇರುಗಳನ್ನು ಮಣ್ಣು ಮುಚ್ಚಿದೆಯೇ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
            "te": "మొక్క మొదలు వద్ద నేల నిర్మాణాన్ని గమనించండి. నేల వదులుగా ఉండి వేర్లను మట్టి కప్పి ఉంచేలా చూసుకోండి."
        }
    elif days_passed < 100:
        stage = {"en": "Tillering Phase", "mr": "फुटवे नियंत्रण अवस्था", "kn": "ಪಿಲಕೆ ನಿರ್ವಹಣೆ ಹಂತ", "te": "పిలకల యాజమాన్య దశ"}
        action = {
            "en": "Perform light earthing-up using a ridge-cultivator. If broad-leaf weeds or nut grass are visible, spray Halosulfuron-methyl at 36g/acre.",
            "mr": "रिजर-कल्टिव्हेटरचा वापर करून हलकी भर द्या. रुंद पानाच्या पिकांचे तण किंवा लव्हाळा दिसल्यास ३६ ग्रॅम/एकर हॅलोसल्फ्युरॉन-मिथाईल फवारा.",
            "kn": "ರಿಡ್ಜ್-ಕಲ್ಟಿವೇಟರ್ ಬಳಸಿ ಲಘುವಾಗಿ ಮಣ್ಣು ಏರಿಸಿ. ಅಗಲವಾದ ಕಳೆಗಳು ಅಥವಾ ಜೇಕು ಹುಲ್ಲು ಕಂಡುಬಂದರೆ ಎಕರೆಗೆ 36g ಹ್ಯಾಲೋಸಲ್ఫ್ಯೂರೋನ್-ಮಿಥೈಲ್ ಸಿಂಪಡಿಸಿ.",
            "te": "రిడ్జ్-కల్టివేటర్ ఉపయోగించి తేలికగా మట్టిని چڑھించండి. వెడల్పాటి కలుపు మొక్కలు లేదా తుంగ కనిపిస్తే ఎకరాకు 36 గ్రాముల హాలోసల్ఫ్యూరాన్-మిథైల్ పిచికారీ చేయండి."
        }
        obs = {
            "en": "Identify and monitor the primary stems. Late, thin, or thread-like tillers must be suppressed.",
            "mr": "मुख्य काड्या ओळखा. उशिरा आलेले, बारीक किंवा दोऱ्यासारखे फुटवे दाबून टाकले पाहिजेत.",
            "kn": "ಪ್ರಾಥಮಿಕ ಜಲ್ಲೆಗಳನ್ನು ಗುರುತಿಸಿ. ತಡವಾಗಿ ಬಂದ, ತೆಳುವಾದ ಅಥವಾ ದಾರದಂತಿರುವ ಪಿಲಕೆಗಳನ್ನು ಹತ್ತಿಕ್ಕಬೇಕು.",
            "te": "ముఖ్యమైన కాండాలను గుర్తించండి. ఆలస్యంగా వచ్చిన, సన్నని పిలకలను అణచివేయాలి."
        }
    elif days_passed < 120:
        stage = {"en": "Tiller Selection", "mr": "मजबूत काड्यांची निवड", "kn": "ಪಿಲಕೆ ಆಯ್ಕೆ ಹಂತ", "te": "పిలకల ఎంపిక దశ"}
        action = {
            "en": "Inject Bio-Bramha Biostimulant via drip system/Drenching to transition the crop into accelerated cell division.",
            "mr": "पिकाला जलद पेशी विभाजनाच्या अवस्थेत नेण्यासाठी ठिबक किंवा ड्रेंचिंगद्वारे बायो-ब्रह्मा बायोस्टिम्युलंट द्या.",
            "kn": "ಬೆಳೆಯನ್ನು ತ್ವರಿత ಜೀವಕೋಶ ವಿಭಜನೆಗೆ ಪರಿವರ್ತಿಸಲು ಡ್ರಿಪ್ ಸಿಸ್ಟಮ್/ಡ್ರೆಂಚಿಂಗ್ ಮೂಲಕ ಬಯೋ-ಬ್ರಹ್ಮ ಬಯೋಸ್ಟಿಮ್ಯುಲಂಟ್ ನೀಡಿ.",
            "te": "పంటను వేగవంతమైన కణ విభజన దశకు మార్చడానికి డ్రిప్ లేదా డ్రెంచింగ్ ద్వారా బయో-బ్రహ్మ బయోస్టిమ్యులెంట్ అందించండి."
        }
        obs = {
            "en": "Confirm that the target density of 1 strong cane per square foot is clear of parasitic tillers.",
            "mr": "प्रति चौरस फुटात १ मजबूत काडीची घनता राखण्यासाठी अनावश्यक फुटवे काढल्याची खात्री करा.",
            "kn": "ಪ್ರತಿ ಚದರ ಅಡಿಗೆ 1 ಬಲವಾದ ಕಬ್ಬಿನ ಗುರಿಯ ಸಾಂದ್ರತೆಯು ಪರಾವಲಂಬಿ ಪಿಲಕೆಗಳಿಂದ ಮುಕ್ತವಾಗಿದೆಯೇ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
            "te": "ప్రతి చదరపు అడుగుకు 1 బలమైన చెరకు ఉండేలా అదనపు పిలకలు లేకుండా చూసుకోండి."
        }
    elif days_passed < 150:
        stage = {"en": "Grand Growth", "mr": "मोठ्या वाढीची अवस्था", "kn": "ಬೃಹತ್ ಬೆಳವಣಿಗೆಯ ಹಂತ", "te": "భారీ ఎదుగుదల దశ"}
        action = {
            "en": "Perform Heavy Earthing Up to bury weak tillers and stabilize primary stems. Apply 20 kg Sulphate of Potash per acre via drip.",
            "mr": "कमकुवत फुटवे गाडण्यासाठी आणि मुख्य काड्या स्थिर करण्यासाठी मोठी भर द्या. ठिबकद्वारे २० किलो सल्फेट ऑफ पोटॅश प्रति एकर द्या.",
            "kn": "ದುರ್ಬಲ ಪಿಲಕೆಗಳನ್ನು ಹೂತುಹಾಕಲು ಮತ್ತು ಪ್ರಾಥಮಿಕ ಕಾಂಡಗಳನ್ನು ಸ್ಥಿರಗೊಳಿಸಲು ಭಾರಿ ಮಣ್ಣು ಏರಿಸುವಿಕೆ ಮಾಡಿ. ಡ್ರಿಪ್ ಮೂಲಕ ಎಕರೆಗೆ 20 ಕೆಜಿ ಸಲ್ಫೇಟ್ ಆಫ್ ಪೊಟ್ಯಾಶ್ ನೀಡಿ.",
            "te": "బలహీనమైన పిలకలను అణచివేయడానికి మరియు ముఖ్య కాండాలను స్థిరపరచడానికి భారీగా మట్టిని چڑھించండి. డ్రిప్ ద్వారా ఎకరాకు 20 కిలోల సల్ఫేట్ ఆఫ్ పొటాష్ వేయండి."
        }
        obs = {
            "en": "Inspect the lower leaf sheaths for early presence of scales or mealybugs. Check internode spacing.",
            "mr": "खालील पानाच्या कोशांवर खवले कीड किंवा पिठ्या ठिपका (mealybugs) चा प्रादुर्भाव तपासा. कांड्यांमधील अंतर तपासा.",
            "kn": "ಕೆಳಗಿನ ಎಲೆಗಳ ಬುಡದಲ್ಲಿ ಹಿಟ್ಟುತಿಗಣೆ ಅಥವಾ ಹುರುಪೆ ಕೀಟಗಳ ಆರಂಭಿಕ ಉಪಸ್ಥಿತಿಯನ್ನು ಪರೀಕ್ಷಿಸಿ. ಕಣ್ಣುಗಳ ನಡುವಿನ ಅಂತರವನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "te": "క్రింది ఆకుల వద్ద పిండినల్లి లేదా పొలుసు కీటకాల ఉనికిని పరిశీలించండి. కణుపుల మధ్య దూరాన్ని తనిఖీ చేయండి."
        }
    elif days_passed < 180:
        stage = {"en": "Internode Elongation", "mr": "कांड्या लांब होण्याची अवस्था", "kn": "ಗೆಣ್ಣು ಉದ್ದವಾಗುವ ಹಂತ", "te": "కణుపుల పొడవు పెరిగే దశ"}
        action = {
            "en": "Spray Orthosilicic Acid (Silicon) at 1ml/L + Boron (20%) at 1g/L to strengthen cane walls and prepare for heavy weight accumulation.",
            "mr": "काडीची साल मजबूत करण्यासाठी आणि वजन वाढवण्यासाठी ऑर्थोसिलिसिक ॲसिड (सिलिकॉन) १ मिली/लिटर + बोरॉन (२०%) १ ग्रॅम/लिटर फवारा.",
            "kn": "ಕಬ್ಬಿನ ಜಲ್ಲೆಯ ಗೋಡೆಗಳನ್ನು ಬಲಪಡಿಸಲು ಮತ್ತು ತೂಕ ಹೆಚ್ಚಳಕ್ಕೆ ತಯಾರಾಗಲು 1ml/L ಆರ್ಥೋಸಿಲಿಸಿಕ್ ಆಸಿಡ್ (ಸಿಲಿಕಾನ್) + 1g/L ಬೋರಾನ್ (20%) ಸಿಂಪಡಿಸಿ.",
            "te": "చెరకు కాండం బలాన్ని పెంచడానికి మరియు బరువు పెరగడానికి 1ml/L ఆర్థోసిలిసిక్ యాసిడ్ (సిలికాన్) + 1g/L బోరాన్ (20%) పిచికారీ చేయండి."
        }
        obs = {
            "en": "Check for any signs of leaning or lodging after strong winds or heavy watering.",
            "mr": "जोराचा वारा किंवा जास्त पाण्यानंतर पीक लोळण्याची किंवा झुकण्याची कोणतीही लक्षणे तपासा.",
            "kn": "ಬಲವಾದ ಗಾಳಿ ಅಥವಾ ಭಾರಿ ನೀರಾವರಿ ನಂತರ ಕಬ್ಬು ವಾಲಿರುವ ಯಾವುದೇ ಚಿಹ್ನೆಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ.",
            "te": "భారీ గాలులు లేదా ఎక్కువ నీటి తడుల తర్వాత చెరకు పడిపోయే సంకేతాలను తనిఖీ చేయండి."
        }
    elif days_passed < 210:
        stage = {"en": "Cane Weight Max", "mr": "वजन वाढवण्याची अवस्था", "kn": "ಕಬ್ಬಿನ ತೂಕ ಗರಿಷ್ಠ ಹಂತ", "te": "చెరకు బరువు గరిష్ట దశ"}
        action = {
            "en": "Execute first de-trashing (remove dry, dead lower leaves) and tie adjacent cane rows together (propping) to prevent tipping.",
            "mr": "वाळलेली खालची पाने काढा (पाचट काढणे) आणि पीक पडू नये म्हणून शेजारील काड्यांच्या ओळी एकत्र बांधा (propping).",
            "kn": "ಒಣಗಿದ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಕಬ್ಬು ಬೀಳದಂತೆ ತಡೆಯಲು ಪಕ್ಕದ ಸಾಲುಗಳನ್ನು ಒಟ್ಟಿಗೆ ಕಟ್ಟಿರಿ (ಪ್ರಾಪಿಂಗ್).",
            "te": "ఎండిపోయిన కింది ఆకులను తొలగించి, చెరకు పడిపోకుండా పక్క పక్క వరుసలను కలిపి కట్టండి."
        }
        obs = {
            "en": "Observe the rind color deepening and check the thickness of the cane diameter.",
            "mr": "काडीचा रंग गडद होणे आणि काडीचा व्यास (जाडी) तपासा.",
            "kn": "ಕಬ್ಬಿನ ಜಲ್ಲೆಯ ಬಣ್ಣ ಗಾಢವಾಗುವುದನ್ನು ಗಮನಿಸಿ ಮತ್ತು ಜಲ್ಲೆಯ ದಪ್ಪವನ್ನು ಪರೀಕ್ಷಿಸಿ.",
            "te": "చెరకు పై తొక్క రంగు ముదురుగా మారడాన్ని గమనించండి మరియు కాండం లావును తనిఖీ చేయండి."
        }
    elif days_passed < 300:
        stage = {"en": "Maturation Start", "mr": "परिपक्वतेची सुरुवात", "kn": "ಪಕ್ವತೆ ಆರಂಭದ ಹಂತ", "te": "పక్వత ప్రారంభ దశ"}
        action = {
            "en": "Spray second round of Silicon + Boron. Reduce water volume slightly via drip, switching to a maintenance irrigation volume.",
            "mr": "सिलिकॉन + बोरॉनची दुसरी फवारणी करा. ठिबकद्वारे पाण्याचे प्रमाण थोडे कमी करा आणि केवळ गरजेपुरतेच पाणी द्या.",
            "kn": "ಸಿಲಿಕಾನ್ + ಬೋರಾನ್ ಎರಡನೇ ಸುತ್ತಿನ ಸಿಂಪಡಣೆ ಮಾಡಿ. ಡ್ರಿಪ್ ಮೂಲಕ ನೀರಿನ ಪ್ರಮಾಣವನ್ನು ಸ್ವಲ್ಪ ಕಡಿಮೆ ಮಾಡಿ, ಕೇವಲ ತೇವಾಂಶ ನಿರ್ವಹಣೆ ಮಾಡಿ.",
            "te": "సిలికాన్ + బోరాన్ రెండవ విడత పిచికారీ చేయండి. డ్రిప్ ద్వారా నీటి పరిమాణాన్ని కొద్దిగా తగ్గించి, కేవలం తేమను కాపాడండి."
        }
        obs = {
            "en": "Monitor brix values using a hand-refractometer.",
            "mr": "हँड-रिफ्रॅक्टोमीटर वापरून ब्रिक्स मूल्यांवर (साखरेचे प्रमाण) लक्ष ठेवा.",
            "kn": "ಹ್ಯಾಂಡ್-ರಿಫ್ರಾಕ್ಟೋಮೀಟರ್ ಬಳಸಿ ಬ್ರಿಕ್ಸ್ ಮೌಲ್ಯಗಳನ್ನು ಗಮನಿಸಿ.",
            "te": "హ్యాండ్-రిఫ్రాక్టోమీటర్ ఉపయోగించి బ్రిక్స్ విలువలను పర్యవేక్షించండి."
        }
    else:
        stage = {"en": "Maturity/Harvest", "mr": "परिपक्वता / काढणी", "kn": "ಕಟಾವು ಹಂತ", "te": "కోత దశ"}
        action = {
            "en": "Stop irrigation entirely 15 days before the scheduled harvest date to force maximum sugar synthesis and concentration.",
            "mr": "साखरेचे प्रमाण जास्तीत जास्त वाढवण्यासाठी ठरलेल्या काढणीच्या तारखेच्या १५ दिवस आधी पाणी देणे पूर्णपणे बंद करा.",
            "kn": "ಗರಿಷ್ಠ ಸಕ್ಕರೆ ಸಾಂದ್ರತೆಯನ್ನು ಹೆಚ್ಚಿಸಲು ನಿಗದಿತ ಕಟಾವು ದಿನಾಂಕಕ್ಕಿಂತ 15 ದಿನಗಳ ಮುಂಚಿತವಾಗಿ ನೀರಾವರಿಯನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ನಿಲ್ಲಿಸಿ.",
            "te": "గరిష్ట చక్కెర శాతాన్ని పెంచడానికి అనుకున్న కోత తేదీకి 15 రోజుల ముందే నీటి తడులను పూర్తిగా నిలిపివేయండి."
        }
        obs = {
            "en": "Target brix reading for harvest: 18-20%.",
            "mr": "काढणीसाठी लक्ष्य ब्रिक्स रीडिंग: १८-२०%.",
            "kn": "ಕಟಾವಿಗೆ ಗುರಿಯ ಬ್ರಿಕ್ಸ್ ರೀಡಿಂಗ್: 18-20%.",
            "te": "కోతకు కావలసిన బ్రిక్స్ రీడింగ్: 18-20%."
        }

    return (
        f"Day {days_passed} — [{stage[l_key]} Stage]\n\n"
        f"🔔 ACTION REQUIRED:\n{action[l_key]}\n\n"
        f"👁️ FIELD OBSERVATION CHECKLIST:\n{obs[l_key]}"
    )

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

class PlotForm(BaseModel):
    farmer_name: str
    phone_number: str
    crop: str
    acreage: int
    date: str
    lang: str = "en"

class AdminLogin(BaseModel):
    password: str

@app.get("/api/plots")
def get_plots(lang: str = "en"):
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
                "advisory": generate_agronomy_rules(r[2], lang, r[4])
            }
            for r in rows
        ]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

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

@app.post("/api/admin/login")
def admin_l