# 🔒 Encrypted Chat (Python + RSA)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![VS Code](https://img.shields.io/badge/Editor-VS%20Code-007ACC.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Security](https://img.shields.io/badge/Encryption-RSA--2048-orange.svg)

A lightweight, end-to-end encrypted chat application built with Python.  
Secured with **RSA-OAEP** and designed for smooth development & debugging inside **VS Code**.
This application was developed as a project for the ENGI 9818: Computer Software Foundations course.

---

## 🚀 Features
- 2048-bit RSA key generation  
- End-to-end encrypted messaging  
- TCP client/server communication  
- Real-time messaging using threads  
- Modular, readable codebase  
- Graceful handling of errors and disconnects  

---

# 🛠️ VS Code Setup

## 1️⃣ Requirements
- **Python 3.10+**  
- **VS Code**  
- VS Code Extensions:
  - *Python*  
  - *Pylance*  

---

## 2️⃣ Install Dependencies
Open **VS Code → Terminal → New Terminal**, then run:

```bash
pip install cryptography

## Features

***2048-bit RSA key generation ***
***End-to-end encrypted communication***
***TCP client/server architecture***
***Real-time messaging via threads***
***Clean modular code (3 small modules)***
***raceful handling of disconnects & decryption errors***

🛠️ VS Code Setup

Install Required Tools
Make sure you have:
Python 3.10+
VS Code
VS Code extensions:
Python (Microsoft)
Pylance (recommended)

3️⃣ Open the Project in VS Code
File → Open Folder → select your project folder

project/
 ├── src/
 │    ├── chat_app.py
 │    ├── socket_handler.py
 │    └── key_manager.py
 ├── keys/
 └── README.md

▶️ Running the Program

1. Run this In two separate teminals first: 
python -m src.chat_app genkeys

It Creates:
keys/private_key.pem
keys/public_key.pem

2. 🖥️ Start the Server
python -m src.chat_app server 5000

3. 💬 Start the Client 
python -m src.chat_app client 127.0.0.1 5000 keys/public_key.pem

4. You can also test if the crypto is working fine: 
python -m src.main test-crypto

⚠️ Limitations
One-to-one chat only
Public keys must be shared manually
Uses pure RSA (no hybrid RSA + AES)

👤 Author
Tanzim Rahman
Siddiq Husain Tashfeen 
ENGI 9818 — Computer Software Foundations