"""# VIT Bhopal Smart Health Portal (VITyarthi Project)

**A comprehensive digital healthcare management system designed to streamline medical services within the university campus.**

## 📖 Simple Overview

This application digitizes the campus health center workflow, allowing students to book appointments and buy medicines online while providing doctors with a digital console to manage patients and issue prescriptions.

## 📝 Description

The **VIT Bhopal Smart Health Portal** is a robust web application developed to modernize campus healthcare. By replacing traditional manual paperwork with an efficient, paperless system, it bridges the gap between **Students**, **Doctors**, and the **Pharmacy**.

The application features gender-based appointment booking (automatically filtering relevant doctors and hostel blocks), a secure doctor console for digital prescribing, and a fully functional E-Pharmacy with a cart system. Doctors can manage patient queues effectively and archive treated cases, while students maintain a persistent medical history with downloadable PDF records. The system leverages Python's core capabilities, including Object-Oriented Programming, file handling, and SQLite database management, to ensure efficiency and data integrity.

## 🚀 Getting Started

### Dependencies

Before running the application, ensure your system meets the following requirements:

* **Operating System:** Windows 10/11, macOS, or Linux.

* **Python:** Version 3.10 or higher.

* **Required Libraries:**

  * `streamlit` (Web Interface)

  * `fpdf` (PDF Generation)

* **Standard Libraries (Pre-installed):** `sqlite3`, `os`, `random`, `json`, `datetime`, `socket`.

### Installing

1. **Download the Project:**
   Create a folder named `VIT_Health_Project` and ensure it contains the following files:

   * `health_app.py` (The main application code)

   * `requirements.txt` (List of dependencies)

   * `vit_logo.jpg` (Required for PDF Header generation)

   * `vit_campus.png` (Required for Sidebar UI)

   * *Reference Docs:* `Problem Statement.pdf`, `Project Screenshots.pdf`, `Project report VIT_Health_app.pdf`

2. **Setup Environment:**
   Open your command prompt or terminal in this folder.

### Executing Program

Follow these step-by-step instructions to run the application:

1. **Open Command Prompt/Terminal:**

   * Navigate to the folder where you saved the files.

   * Example: `cd Desktop/VIT_Health_Project`

2. **Install Dependencies:**
   Run the following command to install the necessary packages:

   ```bash
   pip install -r requirements.txt
   ```

   *(Or manually: `pip install streamlit fpdf`)*

3. **Run the Application:**
   Execute the Streamlit run command:

   ```bash
   streamlit run health_app.py
   ```

4. **Access the Portal:**

   * The app will open automatically in your default web browser.

   * **Local URL:** `http://localhost:8501`

## 📚 Technical Code Implementation (Python Concepts)

This project demonstrates the practical application of the following core Python concepts:

### Input and Output Operations

The application extensively uses I/O operations to interact with the user and the file system.

* **Input:** We use `st.text_input` to capture the Registration Number, `st.number_input` for Age/Weight, and `st.selectbox` for choosing Doctors. This captures raw data from the user interface.

* **Output:** The system outputs data in two ways: displaying text on the screen using `st.write()` and generating files using the `fpdf` library. The `generate_ticket_file()` function writes formatted strings to a binary PDF file, serving as a permanent output document.

### Precedence & Associativity

Operator precedence determines the order in which operations are parsed. This is critical in the Health Tools module.

* **Implementation:** In the **BMI Calculator** function, the formula used is `bmi = weight / (height_m ** 2)`.

* **Explanation:** Python's precedence rules ensure that the exponentiation (`**`) happens before the division (`/`). Without this correct associativity, the health metric calculation would be mathematically incorrect.

### Type Conversion

Data often needs to be converted between types for processing, storage, or display (Type Casting).

* **Implicit Conversion:** Python automatically handles integer-to-float conversion during price calculations in the pharmacy cart (e.g., `total += item['price']`).

* **Explicit Conversion:** We explicitly use `str(date)` to convert the Date object into a string before saving it to the SQLite database. We also use `int(time.time())` to convert the current timestamp into an integer seed for random number generation.

### Core Data Structures

The project utilizes Python's built-in data structures to organize memory efficiently:

* **Lists:** `MEDICINES_DB` is a List of Dictionaries. This mutable structure allows us to store an ordered sequence of medicine items that can be iterated over.

* **Dictionaries:** Used for `SYMPTOM_ADVICE`. It maps a specific key (e.g., 'fever') to a value (medical advice), providing O(1) lookup time for instant retrieval.

* **Tuples:** `CLINIC_TIMINGS` is stored as a Tuple. Since clinic hours do not change during runtime, an immutable tuple ensures data integrity and prevents accidental modification.

### Control Flow Statements

Control flow dictates the logic path of the application based on user decisions.

* **Conditional (If-Else):** Used in `if gender == "Male":`. This logic checks the user's gender and dynamically changes the `available_docs` list to ensure male students only see male doctors and vice versa.

* **Iterative (For Loops):** Used in `for med in MEDICINES_DB:`. This loop iterates through the medicine database to render the catalog cards on the screen dynamically.

### Functions

The code is decomposed into modular functions to improve readability and reusability.

* **Example:** The `book_appointment_db()` function encapsulates all the SQL logic required to save an appointment. Instead of rewriting SQL queries multiple times, we simply call this function with parameters, adhering to the DRY (Don't Repeat Yourself) principle.

### Modules & Packages

The project is built by importing various modules to extend Python's capabilities:

* **Standard Modules:** `sqlite3` (database interactions), `os` (file system checks), `random` (generating unique codes), `json` (data parsing), `datetime`.

* **External Packages:** `streamlit` is imported to build the web interface, and `fpdf` is imported to generate PDF documents.

### Array Data Structure

While Python does not have native arrays like C, Lists function as dynamic arrays in this context.

* **Implementation:** In the E-Pharmacy module, `st.session_state.cart` acts as a dynamic array. We use `append()` to add items to the cart and `pop()` to remove items by index. This mimics array-based stack operations for managing the shopping cart state.

### Object Oriented Programming

The project implements OOP principles to model real-world entities:

* **Classes & Objects:** We defined a `Person` class to hold basic data like Name and Registration Number.

* **Inheritance:** The `Student` class inherits from `Person`. This allows the Student object to reuse the code from Person while adding specific attributes like `gender` and `age`. This promotes code reusability and hierarchical data modeling.

## ❓ Help

Common issues and solutions:

* **"Streamlit is not recognized"**: Ensure Python is added to your system PATH. Try running: `python -m streamlit run health_app.py`

* **"FileNotFoundError"**: Ensure `vit_logo.jpg` and `vit_campus.png` are in the exact same folder as the python script.

* **Database Reset**: If you want to clear all data, simply delete the `vit_health_v6.db` file in the folder. The app will generate a fresh one automatically upon restart.

## 👤 Authors

**Swattik Pradhan**

* Registration No: **25BCE10457**
"""

with open("README.txt", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("README.txt created successfully!")