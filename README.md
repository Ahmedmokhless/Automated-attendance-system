# Automated Student Attendance System Using Facial Recognition 🎓

This is my final year graduation project — a smart, automated student attendance system using real-time facial recognition.

## 🚀 Project Overview

The system allows:
- Student **face registration**
- Real-time **attendance marking** using webcam
- **Exporting attendance reports** (PDF/Excel)
- **Subject and professor management**
- Automated **emailing to professors**

## 🛠️ Built With
- **Python**
- **OpenCV** (LBPH Face Recognizer)
- **SQLite** (Local database)
- **Tkinter** (GUI)
- **Pandas**, **Fpdf**, **XlsxWriter**

## 📁 Features
- GUI app to register students and manage subjects
- Webcam-based attendance detection
- Export daily attendance for each subject
- Send attendance by email to professors
- Separate scripts for each module

## 🔧 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/attendance-face-recognition.git
   cd attendance-face-recognition

2. ```bash
   pip install -r requirements.txt

3. Run the modules:
   ```bash
   Copy
   Edit
   python Register_faces.py          # Register student faces
   python Manage_subjects.py         # Add subjects and professor emails
   python attendance_taker.py        # Start attendance system
   python export_attendance.py       # Export and email reports

📂 Folder Structure

attendance-face-recognition/
├── Register_faces.py
├── Manage_subjects.py
├── attendance_taker.py
├── export_attendance.py
├── start_webserver.py
├── data/
│   ├── trained_model.yml
│   ├── label_mapping.txt
│   └── data_faces_from_camera/
├── attendance.db
├── requirements.txt
└── README.md

Note: Student face data and trained models are not included in this repository to respect privacy.
