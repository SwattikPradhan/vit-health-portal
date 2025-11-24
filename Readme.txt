🏥 VIT Bhopal Health Portal

VIT Bhopal Health Portal is a digital healthcare management system designed to streamline medical services within the university campus. It replaces manual paperwork with an efficient, paperless system connecting Students, Doctors, and the Pharmacy.

📖 Table of Contents

Project Overview

Key Features

Technology Stack

Installation & Setup

How to Use

Project Structure

🚀 Project Overview

The current manual system at the university health center often leads to long queues, lost prescription papers, and slow pharmacy service. This web application solves these issues by:

Digitizing appointment bookings.

Providing a secure dashboard for doctors to prescribe medicine.

Enabling online medicine ordering for students.

Maintaining a permanent digital medical history with PDF downloads.

✨ Key Features

🎓 Student Portal

Smart Appointment Booking:

Gender-based logic: Boys see Male Doctors & Boys' Hostels (Blocks 1-9); Girls see Female Doctors & Girls' Hostels.

Input details like Room No, Contact, and Symptoms (Multi-select).

Instant PDF Ticket: Generates a downloadable PDF appointment pass.

E-Pharmacy:

Browse medicines with real-time prices and stock status.

Add to Cart with Quantity selectors (+ / -).

Secure Checkout: Generates a unique Order Code and a PDF Receipt/Invoice upon checkout.

Medical History:

View past appointments and diagnoses.

Download Prescription: Save official prescriptions sent by doctors as PDFs.

Health Tools:

BMI Calculator and Symptom-based First Aid Helper.

👨‍⚕️ Doctor Console

Secure Workspace: Doctors select their profile to log in.

Live Queue: View pending appointments with patient details (Hostel, Room, Symptoms).

Digital Prescribing: Write prescriptions digitally and send them instantly to the student's dashboard.

Patient Management: "Sent" status indicator and option to Archive/Clear treated patients.

🛠 Technology Stack

Frontend & Backend: Streamlit (Python)

Database: SQLite3 (Local relational database)

PDF Generation: FPDF Library

Styling: Custom CSS (Glassmorphism & Dark Mode)

⚙️ Installation & Setup

To run this project locally on your machine:

1. Prerequisites
Ensure you have Python installed.

2. Clone the Repository (or Download Code)

git clone [https://github.com/your-username/vit-health-portal.git](https://github.com/your-username/vit-health-portal.git)
cd vit-health-portal


3. Install Dependencies

pip install streamlit fpdf


4. Run the App

streamlit run health_app.py


5. Access the App
Open your browser and go to: http://localhost:8501

📱 How to Use

1. Student Mode

Booking: Go to "Book Appointment". Select your gender, fill in your Hostel/Room details, select symptoms, and confirm. Download your PDF Ticket.

Pharmacy: Go to "Pharmacy". Enter your Registration ID to unlock. Add items to your cart and checkout to get your PDF Receipt.

Records: Go to "Medical Records". Search your Reg ID to see past advice and download Prescription PDFs.

2. Doctor Mode

Switch the Login Mode in the sidebar to Doctor Console.

Select the appropriate doctor profile (e.g., General Physician).

Check "Access Dashboard".

Expand a patient card, write the prescription/advice, and click "Send".

Once done, click "Delete/Clear" to archive the patient.
Project Structure

VIT_Health_Project/
├── health_app.py       # Main Application Code
├── requirements.txt    # List of libraries (streamlit, fpdf)
├── vit_logo.jpg        # University Logo for PDF Headers
├── vit_campus.png      # Sidebar Image
├── vit_health_v6.db    # SQLite Database (Auto-generated)
└── README.md           # Project Documentation
