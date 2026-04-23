# 🛡️ FaceLogger - AI Access Control System

> An intelligent access control system powered by Computer Vision, Real-Time Analytics, and IoT concepts.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=for-the-badge&logo=opencv)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

## 📸 Screenshots

<img width="1636" height="738" alt="image" src="https://github.com/user-attachments/assets/414bc987-b0ff-4310-8175-7147b62d07f6" />


## 🚀 About the Project

**FaceLogger** is a full-stack solution designed to automate reception desks, gyms, and restricted areas. It replaces traditional ID cards with facial biometrics, providing a seamless and secure entry experience.

**Key Features:**
* 🔐 **Facial Recognition:** Implements LBPH (Local Binary Patterns Histograms) algorithm for robust user identification.
* ⚡ **Real-Time Logging:** Instant data transmission from the camera client to the web dashboard via REST API.
* 🖥️ **Interactive Mode:** Visual feedback (Green/Red overlays) for the end-user.
* 📊 **Analytics Dashboard:** Web interface to monitor access logs, timestamps, and captured snapshots.
* ⚙️ **IoT Hardware Integration:** Physical access using Serial communication to trigger micro servo motor and feedback LEDs by Arduino.



## 🛠️ Tech Stack

**Software:**
* **Computer Vision:** OpenCV (Face detection & recognition)
* **Backend API:** Python FastAPI & `pyserial`
* **Database:** SQLite (Lightweight local storage)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

**Hardware / IoT:**
* **Microcontroller:** Arduino Uno
* **Actuators:** Micro Servo Motor (Turnstile simulation)
* **Visual Feedback:** Green/Red LEDs

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

## 🔌 Hardware Setup (IoT Module)

The system can work 100% digital, but includes support to physical hardware. The python script communicates with an Arduino by USB, sending binary signals

* `1` **(Match found):** Turn the green LED on and rotates the servo to 90°
* `0` **(Access Denied):** Quickly turn the red LED on and keep the servo locked in 0°.

*(Você pode incluir uma foto do seu circuito montado na protoboard aqui!)*

Developed by Icaro de Souza 🚀 
https://www.linkedin.com/in/icaro-souza-ti/

https://github.com/icarodev10
