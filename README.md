# 🛡️ FaceLogger - AI Access Control System

> An intelligent access control system powered by Computer Vision, Real-Time Analytics, and IoT concepts.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=for-the-badge&logo=opencv)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

## 📸 Screenshots

| Access Terminal (Totem) | Admin Dashboard |
|:---:|:---:|
| ![Totem View](https://placehold.co/600x400?text=Totem+Screenshot) | ![Dashboard View](https://placehold.co/600x400?text=Dashboard+Screenshot) |

## 🚀 About the Project

**FaceLogger** is a full-stack solution designed to automate reception desks, gyms, and restricted areas. It replaces traditional ID cards with facial biometrics, providing a seamless and secure entry experience.

**Key Features:**
* 🔐 **Facial Recognition:** Implements LBPH (Local Binary Patterns Histograms) algorithm for robust user identification.
* ⚡ **Real-Time Logging:** Instant data transmission from the camera client to the web dashboard via REST API.
* 🖥️ **Interactive Kiosk Mode:** Visual feedback (Green/Red overlays) for the end-user.
* 📊 **Analytics Dashboard:** Web interface to monitor access logs, timestamps, and captured snapshots.

## 🛠️ Tech Stack

* **Computer Vision:** OpenCV (Face detection & recognition)
* **Backend API:** Python FastAPI
* **Database:** SQLite (Lightweight local storage)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API for dynamic updates)

## 📦 Installation & Setup

### Prerequisites
* Python 3.x installed
* A working webcam

### Step 1: Clone the repository

git clone [https://github.com/icarodev10/FaceLogger.git](https://github.com/icarodev10/FaceLogger.git)
cd FaceLogger

### Step 2: Install dependencies

pip install -r requirements.txt

### Step 3: Initialize the System
Start the API & Dashboard: Open a terminal and run:

python api.py
The Dashboard will be available at: http://localhost:8000

Register a User (Required for first run): Open a second terminal and run:

python gerenciador.py
Select option 1 and follow the instructions to capture your face and train the model.

Start the Camera Totem: Run the camera client:

python camera_web.py
The Camera UI will be available at: http://localhost:5000

⚙️ How it works
Enrollment: The gerenciador.py script captures 30 samples of the user's face and generates a trainer.yml model.

Detection: The camera_web.py captures video frames and compares them against the trained model.

Authorization: If a match is found (Confidence < 60), a request is sent to the API.

Logging: The API saves the event and the base64 image to the database, updating the Dashboard instantly.

Developed by Icaro de Souza 🚀 
https://www.linkedin.com/in/icaro-souza-ti/

https://github.com/icarodev10