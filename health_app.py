import streamlit as st
import sqlite3
import os
import random
import socket
import base64
import string
import json
import time as system_time
import re
from datetime import datetime
from fpdf import FPDF
st.set_page_config(
    page_title="VIT Bhopal Health Portal", 
    layout="wide", 
    page_icon="🏥",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #e0e0e0;
    }
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
    }
    .stExpander, form.stForm, .stTabs, div[data-testid="stMetricValue"], .css-1r6slb0 {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        padding: 20px;
        margin-bottom: 20px;
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] .css-17lntkn, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] li {
        color: #d1d1d1 !important;
    }

    div[data-testid="stNumberInput"] input {
        text-align: center;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 4px 15px rgba(0, 198, 255, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.7);
        background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%);
        color: white;
    }

    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.3) !important; 
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
    }
    
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: #ffffff !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stMultiSelect div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
    }
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #00c6ff !important;
        color: white !important;
    }

    label, .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label, .stTextArea label, .stMultiSelect label {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 1rem;
    }

    h1 {
        background: -webkit-linear-gradient(45deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
    }
    h2, h3 {
        color: #ffffff !important;
    }

    .stAlert {
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: white;
    }
    .stDataFrame {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 10px;
        color: #333;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00c6ff !important;
        background: transparent !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

CLINIC_TIMINGS = ("09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "04:00 PM", "06:00 PM")

DOCTORS_MALE = ["General Physician (Male)", "Orthopedist (Male)"]
DOCTORS_FEMALE = ["General Physician (Female)"]

HEALTH_FACTS = [
    "💧 Dehydration can negatively affect your mood and energy levels.",
    "❤️ Your heart beats around 100,000 times a day.",
    "☀️ Walking outside for 20 minutes can boost your Vitamin D levels.",
    "🥪 Drinking water 30 minutes before a meal helps digestion.",
    "🧼 Sanitary hygiene is crucial to prevent UTIs.",
    "🥬 Iron deficiency is common in students; eat spinach and jaggery.",
    "🧠 Sleep deprivation can lower your immune system.",
    "🍎 An apple a day actually does help keep the doctor away due to fiber content.",
    "🏃‍♂️ 30 minutes of daily exercise reduces heart disease risk significantly."
]

MEDICINES_DB = [
    {"name": "Stayfree/Whisper Pads", "dosage": "Pack of 7", "type": "Sanitary", "stock": 150, "price": 45},
    {"name": "Meftal-Spas", "dosage": "Tablet", "type": "Pain/Period", "stock": 80, "price": 5},
    {"name": "V-Wash", "dosage": "Intimate Wash", "type": "Sanitary", "stock": 40, "price": 180},
    {"name": "Cranberry Sachet", "dosage": "Sachet", "type": "UTI", "stock": 30, "price": 40},
    {"name": "Oxygen Gas", "dosage": "Cylinder", "type": "Emergency", "stock": 5, "price": 0},
    {"name": "Lignocaine 5%", "dosage": "Gel", "type": "Anesthetic", "stock": 10, "price": 35},
    {"name": "Adrenaline", "dosage": "Inj", "type": "Emergency", "stock": 15, "price": 25},
    {"name": "Atropine", "dosage": "Inj", "type": "Emergency", "stock": 10, "price": 15},
    {"name": "Magnesium Sulfate", "dosage": "Inj", "type": "Emergency", "stock": 10, "price": 20},
    {"name": "Paracetamol", "dosage": "500mg Tablet", "type": "Pain/Fever", "stock": 500, "price": 2},
    {"name": "Paracetamol Syrup", "dosage": "125mg/5ml", "type": "Pain/Fever", "stock": 50, "price": 35},
    {"name": "Aspirin", "dosage": "75mg Tablet", "type": "Pain/Cardiac", "stock": 100, "price": 2},
    {"name": "Diclofenac", "dosage": "50mg Tablet", "type": "Pain", "stock": 150, "price": 4},
    {"name": "Ibuprofen", "dosage": "200mg Tablet", "type": "Pain", "stock": 120, "price": 3},
    {"name": "Moov Spray", "dosage": "Spray", "type": "Pain", "stock": 30, "price": 150},
    {"name": "Levocetirizine", "dosage": "5mg Tablet", "type": "Allergy", "stock": 200, "price": 5},
    {"name": "Hydrocortisone", "dosage": "100mg Inj", "type": "Allergy", "stock": 20, "price": 45},
    {"name": "Pheniramine (Avil)", "dosage": "Inj", "type": "Allergy", "stock": 30, "price": 10},
    {"name": "Vicks VapoRub", "dosage": "Balm", "type": "Cold", "stock": 50, "price": 45},
    {"name": "Vicks Inhaler", "dosage": "Inhaler", "type": "Cold", "stock": 60, "price": 60},
    {"name": "Diazepam", "dosage": "5mg Tablet", "type": "Neurological", "stock": 20, "price": 10},
    {"name": "Phenytoin", "dosage": "50mg Tablet", "type": "Neurological", "stock": 30, "price": 8},
    {"name": "Sodium Valproate", "dosage": "200mg Tablet", "type": "Neurological", "stock": 30, "price": 12},
    {"name": "Amoxicillin", "dosage": "500mg Cap", "type": "Antibiotic", "stock": 150, "price": 10},
    {"name": "Azithromycin", "dosage": "500mg Tab", "type": "Antibiotic", "stock": 100, "price": 20},
    {"name": "Metronidazole", "dosage": "400mg Tab", "type": "Antibiotic", "stock": 100, "price": 6},
    {"name": "Doxycycline", "dosage": "100mg Cap", "type": "Antibiotic", "stock": 80, "price": 7},
    {"name": "Clotrimazole", "dosage": "Cream", "type": "Antifungal", "stock": 40, "price": 45},
    {"name": "Fluconazole", "dosage": "150mg Tab", "type": "Antifungal", "stock": 30, "price": 15},
    {"name": "Albendazole", "dosage": "400mg Tab", "type": "Antiparasitic", "stock": 100, "price": 10},
    {"name": "Atenolol", "dosage": "50mg Tablet", "type": "Cardiovascular", "stock": 50, "price": 5},
    {"name": "Amlodipine", "dosage": "5mg Tablet", "type": "Cardiovascular", "stock": 60, "price": 4},
    {"name": "Telmisartan", "dosage": "40mg Tablet", "type": "Cardiovascular", "stock": 50, "price": 8},
    {"name": "Atorvastatin", "dosage": "10mg Tablet", "type": "Cardiovascular", "stock": 50, "price": 10},
    {"name": "Metformin", "dosage": "500mg Tablet", "type": "Diabetes", "stock": 80, "price": 3},
    {"name": "Glimepiride", "dosage": "2mg Tablet", "type": "Diabetes", "stock": 40, "price": 5},
    {"name": "Levothyroxine", "dosage": "50mcg Tablet", "type": "Thyroid", "stock": 30, "price": 4},
    {"name": "Salbutamol", "dosage": "2mg Tablet", "type": "Respiratory", "stock": 50, "price": 2},
    {"name": "Salbutamol Nebulizer", "dosage": "Solution", "type": "Respiratory", "stock": 20, "price": 15},
    {"name": "Dextromethorphan", "dosage": "Syrup", "type": "Respiratory", "stock": 40, "price": 60},
    {"name": "Budesonide", "dosage": "Nebulizer Sol", "type": "Respiratory", "stock": 15, "price": 25},
    {"name": "Ranitidine", "dosage": "150mg Tab", "type": "Gastrointestinal", "stock": 200, "price": 3},
    {"name": "Omeprazole", "dosage": "20mg Cap", "type": "Gastrointestinal", "stock": 150, "price": 5},
    {"name": "Ondansetron", "dosage": "4mg Tablet", "type": "Gastrointestinal", "stock": 80, "price": 5},
    {"name": "ORS", "dosage": "Sachet", "type": "Hydration", "stock": 500, "price": 20},
    {"name": "Domperidone", "dosage": "Tablet", "type": "Gastrointestinal", "stock": 60, "price": 4},
    {"name": "Glucon-D", "dosage": "Powder", "type": "Energy", "stock": 50, "price": 55},
    {"name": "Ciprofloxacin Drops", "dosage": "Eye/Ear Drops", "type": "Eye/ENT", "stock": 40, "price": 25},
    {"name": "Silver Sulphadiazine", "dosage": "Cream", "type": "Skin", "stock": 20, "price": 40},
    {"name": "Betamethasone", "dosage": "Cream", "type": "Skin", "stock": 30, "price": 25},
    {"name": "Calamine Lotion", "dosage": "Lotion", "type": "Skin", "stock": 30, "price": 35},
    {"name": "Povidone Iodine", "dosage": "Ointment", "type": "Antiseptic", "stock": 50, "price": 30},
    {"name": "Boroline", "dosage": "Cream", "type": "Skin", "stock": 60, "price": 40},
    {"name": "Vitamin C", "dosage": "100mg Tab", "type": "Vitamin", "stock": 200, "price": 2},
    {"name": "Calcium Carbonate", "dosage": "500mg Tab", "type": "Supplement", "stock": 150, "price": 5},
    {"name": "Vitamin D3", "dosage": "60k IU Tab", "type": "Vitamin", "stock": 100, "price": 30},
    {"name": "B Complex", "dosage": "Tablet", "type": "Vitamin", "stock": 200, "price": 3},
]

SYMPTOM_ADVICE = {
    "fever": "Take 1 Dolo-650. Drink plenty of water. Rest.",
    "headache": "Apply balm or take rest. Take Paracetamol if severe.",
    "period pain": "Take Meftal-Spas. Use a hot water bag. Rest.",
    "cramps": "Hydrate well. Take Meftal-Spas if due to periods.",
    "cold": "Steam inhalation. Use Vicks VapoRub or Inhaler.",
    "stomach pain": "Avoid spicy food. Drink warm water. Take Ranitidine.",
    "injury": "Clean with Hydrogen Peroxide. Apply Betadine/Boroline.",
    "dehydration": "Drink ORS mixed in water. Rest in shade.",
}

class Person:
    def __init__(self, name, reg_no):
        self.name = name
        self.reg_no = reg_no

class Student(Person):
    def __init__(self, name, reg_no, age, gender):
        super().__init__(name, reg_no)
        self.age = int(age)
        self.gender = gender

    def calculate_bmi(self, weight, height_cm):
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2) 
        return round(bmi, 2)

DB_FILE = 'vit_health_v6.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT,
            name TEXT,
            gender TEXT,
            hostel_no TEXT,
            room_no TEXT,
            parent_contact TEXT,
            date TEXT,
            time TEXT,
            doctor TEXT,
            reason TEXT,
            advice TEXT,
            doctor_visible INTEGER DEFAULT 1
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT,
            items TEXT,
            total_amount REAL,
            order_code TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def book_appointment_db(student_obj, hostel_no, room_no, parent_contact, date, time, doctor, reason):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO appointments (reg_no, name, gender, hostel_no, room_no, parent_contact, date, time, doctor, reason, advice, doctor_visible) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
              (student_obj.reg_no, student_obj.name, student_obj.gender, hostel_no, room_no, parent_contact, str(date), time, doctor, reason, "Pending", 1))
    conn.commit()
    conn.close()

def place_order_db(reg_no, items, total, code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    items_json = json.dumps(items)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO orders (reg_no, items, total_amount, order_code, date) VALUES (?, ?, ?, ?, ?)",
              (reg_no, items_json, total, code, date_str))
    conn.commit()
    conn.close()

def get_order_history(reg_no):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT date, items, total_amount, order_code FROM orders WHERE reg_no = ? ORDER BY id DESC", (reg_no,))
    data = c.fetchall()
    conn.close()
    return data

def get_doctor_appointments(doctor_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Only fetch appointments that are visible to doctor
    c.execute("SELECT id, reg_no, name, gender, date, time, reason, advice, hostel_no, room_no FROM appointments WHERE doctor = ? AND doctor_visible = 1", (doctor_name,))
    data = c.fetchall()
    conn.close()
    return data

def update_doctor_advice(appt_id, advice_text):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE appointments SET advice = ? WHERE id = ?", (advice_text, appt_id))
    conn.commit()
    conn.close()

def archive_appointment(appt_id):
    """Hides appointment from doctor but keeps it for student"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE appointments SET doctor_visible = 0 WHERE id = ?", (appt_id,))
    conn.commit()
    conn.close()

def get_student_history(reg_no):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT date, time, doctor, reason, advice, name FROM appointments WHERE reg_no = ?", (reg_no,))
    data = c.fetchall()
    conn.close()
    return data

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_ticket_file(student_obj, hostel_no, room_no, parent_contact, date, time, doctor):
    filename = f"Ticket_{student_obj.reg_no}.pdf"
    pdf = FPDF()
    pdf.add_page()
    
    if os.path.exists("vit_logo.jpg"):
        try:
            pdf.image("vit_logo.jpg", x=10, y=8, w=30)
            pdf.ln(20)
        except:
            pass

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "VIT BHOPAL UNIVERSITY - HEALTH CENTRE", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "APPOINTMENT TICKET", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 12)
    
    def add_field(label, value):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(50, 10, label, border=0)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, str(value), ln=True)

    add_field("Date of Issue:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    add_field("Student Name:", student_obj.name)
    add_field("Registration No:", student_obj.reg_no)
    add_field("Gender:", student_obj.gender)
    add_field("Hostel Info:", f"{hostel_no} - Room {room_no}")
    add_field("Contact:", parent_contact)
    
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    add_field("Doctor Assigned:", doctor)
    add_field("Appointment Slot:", f"{date} @ {time}")
    
    pdf.output(filename)
    return filename

def generate_prescription_pdf(patient_name, doctor_name, advice, date):
    filename = f"Prescription_{random.randint(1000,9999)}.pdf"
    pdf = FPDF()
    pdf.add_page()
    
    if os.path.exists("vit_logo.jpg"):
        try:
            pdf.image("vit_logo.jpg", x=10, y=8, w=30)
            pdf.ln(20)
        except:
            pass

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "VIT BHOPAL - OFFICIAL PRESCRIPTION", ln=True, align='C')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Fixed line overlap issue
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {date}", ln=True)
    pdf.cell(0, 10, f"Doctor: {doctor_name}", ln=True)
    pdf.cell(0, 10, f"Patient: {patient_name}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Rx / Advice:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, advice)
    
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "This is a digitally generated prescription.", ln=True, align='C')
    
    pdf.output(filename)
    return filename

def generate_order_invoice_pdf(order_code, date, items_list, total):
    filename = f"Invoice_{order_code}.pdf"
    pdf = FPDF()
    pdf.add_page()
    
    if os.path.exists("vit_logo.jpg"):
        try:
            pdf.image("vit_logo.jpg", x=10, y=8, w=30)
            pdf.ln(20)
        except:
            pass

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "VIT BHOPAL PHARMACY - RECEIPT", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {date}", ln=True)
    pdf.cell(0, 10, f"Order Code: {order_code}", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Table Headers
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Item Name", border=1)
    pdf.cell(30, 10, "Qty", border=1, align='C')
    pdf.cell(30, 10, "Price", border=1, align='C')
    pdf.cell(30, 10, "Total", border=1, align='C', ln=True)
    
    # Table Rows
    pdf.set_font("Arial", "", 12)
    for item in items_list:
        if isinstance(item, dict):
            name = item.get('name', 'Unknown')
            qty = str(item.get('qty', 1))
            price = str(item.get('price', 0))
            subtotal = str(item.get('price', 0) * item.get('qty', 1))
            
            pdf.cell(100, 10, name, border=1)
            pdf.cell(30, 10, qty, border=1, align='C')
            pdf.cell(30, 10, price, border=1, align='C')
            pdf.cell(30, 10, subtotal, border=1, align='C', ln=True)
        else:
            # Fallback for old text data
            pdf.cell(100, 10, str(item), border=1)
            pdf.cell(30, 10, "-", border=1, align='C')
            pdf.cell(30, 10, "-", border=1, align='C')
            pdf.cell(30, 10, "-", border=1, align='C', ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(160, 10, "Grand Total:", align='R')
    pdf.cell(30, 10, f"Rs. {total}", align='C', ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Please show this receipt at the pharmacy counter to collect medicines.", ln=True, align='C')
    
    pdf.output(filename)
    return filename

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    init_db()
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'pharmacy_unlocked' not in st.session_state:
        st.session_state.pharmacy_unlocked = False
    if 'current_reg_no' not in st.session_state:
        st.session_state.current_reg_no = ""

    logo_path = "vit_logo.jpg"
    campus_path = "vit_campus.png"

    col1, col2 = st.columns([1, 5])
    with col1:
        if os.path.exists(logo_path):
            try:
                img_base64 = get_base64_image(logo_path)
                st.markdown(f"""<div style="background-color: white; padding: 10px; border-radius: 15px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.2);"><img src="data:image/jpeg;base64,{img_base64}" width="120" style="display: block;"></div>""", unsafe_allow_html=True)
            except: st.write("🏥")
        else: st.write("🏥")
    with col2:
        st.markdown("# VIT Bhopal University Health Centre")
    
    if os.path.exists(campus_path):
        st.sidebar.image(campus_path, use_container_width=True)
    else:
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3004/3004458.png", width=100)
        
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Login Mode", ["Student Portal", "Doctor Console"])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Daily Health Tip")
    
    fact_index = int(system_time.time() / 10) % len(HEALTH_FACTS)
    st.sidebar.success(HEALTH_FACTS[fact_index])
    
    with st.sidebar.expander("📱 Connect via Mobile"):
        ip = get_local_ip()
        st.code(f"http://{ip}:8501")

    if app_mode == "Student Portal":
        st.markdown("## 🎓 Student Dashboard")
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Book Appointment", "📂 Medical Records", "💊 Pharmacy (Buy)", "🛠️ Health Tools"])

        with tab1:
            st.markdown("### 📝 Book Your Slot")
            
            st.markdown("#### Personal Information")
            c_gen, c_filler = st.columns([1, 3])
            with c_gen:
                gender = st.radio("Select Gender", ["Male", "Female"], horizontal=True)

            with st.form("booking_form"):
                c1, c2 = st.columns(2)
                reg_no = c1.text_input("Registration Number", placeholder="21BCE1001")
                name = c2.text_input("Full Name")
                
                c3, c4 = st.columns(2)
                age = c3.number_input("Age", 16, 30, 19)
                
                if gender == "Male":
                    available_docs = DOCTORS_MALE
                    hostel_opts = [f"Boys Block {i}" for i in range(1, 9)] 
                else:
                    available_docs = DOCTORS_FEMALE
                    hostel_opts = ["Girls Block 1", "Girls Block 2", "Special Block"]
                
                doctor = c4.selectbox("Select Doctor", available_docs)
                
                c5, c6 = st.columns(2)
                hostel_no = c5.selectbox("Hostel Block", hostel_opts)
                room_no = c6.text_input("Room Number", placeholder="e.g., B110, A234")
                
                parent_contact = st.text_input("Contact Number:", placeholder="+91 9876543210")
                
                d1, d2 = st.columns(2)
                date = d1.date_input("Date of Visit")
                appt_time = d2.selectbox("Preferred Time", CLINIC_TIMINGS)
                
                st.markdown("### Symptoms Selection")
                symptom_options = ["Fever", "Cold/Cough", "Headache", "Stomach Pain", "Body Pain", "Injury/Cut", "Skin Rash", "Dizziness", "Dehydration", "Other"]
                selected_symptoms = st.multiselect("Select your symptoms", symptom_options, label_visibility="collapsed")
                
                other_reason = st.text_area("Additional Details (Optional)", placeholder="E.g. High fever since last night...")
                
                reason = ", ".join(selected_symptoms)
                if other_reason:
                    reason += f" | Details: {other_reason}"
                
                submitted = st.form_submit_button("Confirm Appointment")
                
            if submitted:
                if reg_no and name and reason and room_no and parent_contact:
                    student = Student(name, reg_no, age, gender)
                    book_appointment_db(student, hostel_no, room_no, parent_contact, date, appt_time, doctor, reason)
                    file_path = generate_ticket_file(student, hostel_no, room_no, parent_contact, date, appt_time, doctor)
                    st.success(f"✅ Appointment Confirmed with {doctor}!")
                    with open(file_path, "rb") as f:
                        st.download_button("📩 Download Ticket (PDF)", f, file_name=file_path, mime="application/pdf")
                else:
                    st.error("⚠️ Please fill all details including Hostel & Parent Contact.")

        with tab2:
            st.markdown("### 📂 Medical History")
            search_reg = st.text_input("Enter Reg No to search records", placeholder="21BCE1001")
            if st.button("🔍 Search"):
                history = get_student_history(search_reg)
                if history:
                    for rec in history:
                        # rec: date, time, doctor, reason, advice, name
                        with st.expander(f"{rec[0]} - {rec[2]}"):
                            st.info(f"📅 {rec[0]} | ⏰ {rec[1]}")
                            st.write(f"🤒 **Issue:** {rec[3]}")
                            if rec[4] == "Pending":
                                st.warning("⚠️ Advice: Pending")
                            else:
                                st.success("✅ **Doctor's Advice:**")
                                st.code(rec[4])
                                pres_pdf = generate_prescription_pdf(rec[5], rec[2], rec[4], rec[0])
                                with open(pres_pdf, "rb") as f:
                                    st.download_button("📄 Download Prescription (PDF)", f, key=f"pres_{rec[0]}_{rec[1]}", file_name=pres_pdf, mime="application/pdf")
                else:
                    st.warning("No records found.")

        with tab3:
            st.markdown("### 💊 Buy Medicines")
            
            if not st.session_state.pharmacy_unlocked:
                st.info("🔒 Enter Registration ID to Access Pharmacy")
                verify_reg = st.text_input("Registration ID", key="pharm_reg")
                
                if st.button("🔓 Enter Pharmacy"):
                    if verify_reg:
                        st.session_state.pharmacy_unlocked = True
                        st.session_state.current_reg_no = verify_reg
                        st.success(f"✅ Welcome, {verify_reg}!")
                        st.rerun()
                    else:
                        st.error("❌ Please enter Registration ID")
            else:
                pharm_tab1, pharm_tab2 = st.tabs(["🛍️ Shop Medicines", "📜 Order History"])
                
                with pharm_tab1:
                    col_shop, col_cart = st.columns([1.8, 1.2])
                    
                    with col_shop:
                        st.subheader("Medicine Catalog")
                        for med in MEDICINES_DB:
                            with st.container():
                                mc1, mc2, mc3, mc4 = st.columns([3, 2, 2, 2])
                                mc1.write(f"**{med['name']}**")
                                mc1.caption(f"({med['type']})")
                                mc2.write(f"₹{med['price']}")
                                
                                qty = mc3.number_input("Qty", min_value=1, max_value=10, value=1, key=f"qty_{med['name']}", label_visibility="collapsed")
                                
                                if mc4.button("Add ➕", key=f"add_{med['name']}"):
                                    found = False
                                    for item in st.session_state.cart:
                                        if item['name'] == med['name']:
                                            item['qty'] += qty
                                            found = True
                                            break
                                    if not found:
                                        new_item = med.copy()
                                        new_item['qty'] = qty
                                        st.session_state.cart.append(new_item)
                                    
                                    st.toast(f"Added {qty} x {med['name']} to cart", icon="🛒")
                    
                    with col_cart:
                        st.subheader("Your Cart")
                        if st.session_state.cart:
                            total = 0
                            cart_items_names = []
                            
                            for index, item in enumerate(st.session_state.cart):
                                with st.container():
                                    c1, c2, c3 = st.columns([3, 2, 2])
                                    item_total = item['price'] * item['qty']
                                    total += item_total
                                    
                                    # Store full object for detailed invoice
                                    cart_items_names.append(item) 
                                    
                                    c1.write(f"**{item['name']}**")
                                    c1.caption(f"₹{item['price']} x {item['qty']} = ₹{item_total}")
                                    
                                    with c2:
                                        if st.button("➖", key=f"dec_{index}", use_container_width=True):
                                            if item['qty'] > 1:
                                                item['qty'] -= 1
                                            else:
                                                st.session_state.cart.pop(index)
                                            st.rerun()
                                    with c3:
                                        if st.button("➕", key=f"inc_{index}", use_container_width=True):
                                            item['qty'] += 1
                                            st.rerun()
                                    
                                st.divider()
                            
                            st.metric("Grand Total", f"₹{total}")
                            
                            if st.button("✅ Checkout", use_container_width=True):
                                order_code = generate_code()
                                place_order_db(st.session_state.current_reg_no, cart_items_names, total, order_code)
                                
                                st.session_state.cart = []
                                st.balloons()
                                st.success("Order Placed Successfully!")
                                st.markdown(f"""
                                    <div style="background-color: #2ecc71; padding: 20px; border-radius: 10px; text-align: center; color: white;">
                                        <h3>Order Confirmed!</h3>
                                        <p>Please show this code at the pharmacy counter:</p>
                                        <h1 style="color: white; font-size: 40px; letter-spacing: 5px;">{order_code}</h1>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("Your cart is empty.")
                            st.markdown("Select items from the catalog to get started.")
                
                with pharm_tab2:
                    st.subheader(f"Order History for {st.session_state.current_reg_no}")
                    orders = get_order_history(st.session_state.current_reg_no)
                    if orders:
                        for order in orders:
                            # order: date, items, total, code
                            with st.expander(f"Order Date: {order[0]} - ₹{order[2]}"):
                                st.info(f"🔑 **Pickup Code:** {order[3]}")
                                items_list = json.loads(order[1])
                                st.write("**Items Purchased:**")
                                for it in items_list:
                                    if isinstance(it, dict):
                                        st.write(f"• {it['name']} (x{it['qty']}) - ₹{it['price']*it['qty']}")
                                    else:
                                        st.write(f"• {it}")
                                
                                inv_pdf = generate_order_invoice_pdf(order[3], order[0], items_list, order[2])
                                with open(inv_pdf, "rb") as f:
                                    st.download_button("🧾 Download Receipt (PDF)", f, key=f"inv_{order[3]}", file_name=inv_pdf, mime="application/pdf")
                    else:
                        st.info("No past orders found.")
                
                st.markdown("---")
                if st.button("🔒 Logout"):
                    st.session_state.pharmacy_unlocked = False
                    st.session_state.current_reg_no = ""
                    st.session_state.cart = []
                    st.rerun()

        with tab4:
            st.markdown("### 🛠️ Health Tools")
            tool = st.radio("Select Tool", ["⚖️ BMI Calculator", "🩺 First Aid Helper"], horizontal=True)
            if tool == "⚖️ BMI Calculator":
                w = st.number_input("Weight (kg)", 30.0)
                h = st.number_input("Height (cm)", 100.0)
                if st.button("Calculate BMI"):
                    st.metric("BMI", f"{round(w / ((h/100)**2), 2)}")
            else:
                st.subheader("🩺 First Aid Helper")
                symptom_keys = list(SYMPTOM_ADVICE.keys())
                symptom_choice = st.selectbox("Select Symptom", ["Select..."] + symptom_keys)
                
                if st.button("Get Advice"):
                    if symptom_choice != "Select...":
                        st.info(f"💡 **Suggestion:** {SYMPTOM_ADVICE.get(symptom_choice)}")
                    else:
                        st.warning("Please select a symptom first.")

    elif app_mode == "Doctor Console":
        st.markdown("## 👨‍⚕️ Doctor's Workspace")
        doc_login = st.selectbox("Select Profile", DOCTORS_MALE + DOCTORS_FEMALE)
        
        if st.checkbox("🔓 Access Dashboard"):
            st.success(f"Welcome back, {doc_login}!")
            appointments = get_doctor_appointments(doc_login)
            
            if appointments:
                for appt in appointments:
                    # appt: id, reg_no, name, gender, date, time, reason, advice, hostel_no, room_no
                    with st.expander(f"Patient: {appt[2]} ({appt[1]})", expanded=True):
                        st.write(f"🏠 **Hostel:** {appt[8]} | **Room:** {appt[9]}")
                        st.write(f"🤒 **Issue:** {appt[6]}")
                        current_advice = appt[7]
                        
                        if current_advice != "Pending":
                            st.success("✅ Prescription Sent")
                            st.text_area("Sent Advice:", value=current_advice, disabled=True, key=f"read_{appt[0]}")
                            if st.button("🗑️ Delete / Clear", key=f"del_{appt[0]}"):
                                archive_appointment(appt[0])
                                st.rerun()
                        else:
                            default_text = "Rx:\n1. [Medicine Name] - [Dosage] - [Timing]\n\nAdvice: Rest well."
                            new_advice = st.text_area(f"Prescription for {appt[2]}", value=default_text, height=150, key=appt[0])
                            
                            if st.button(f"✅ Send Prescription to {appt[2]}", key=f"btn_{appt[0]}"):
                                update_doctor_advice(appt[0], new_advice)
                                st.success("Prescription Sent Successfully!")
                                st.rerun()
            else:
                st.info("No pending appointments.")

if __name__ == "__main__":
    main()