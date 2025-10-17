# Cryptography Chat 🔒

A secure, peer-to-peer (P2P) command-line chat application built with Python. This project uses RSA public-key cryptography to ensure that all messages are sent with end-to-end encryption, guaranteeing confidentiality and privacy.

This application was developed as a project for the ENGI 9818: Computer Software Foundations course.

## Features

***RSA Key Generation:** Users can generate their own unique 2048-bit RSA public/private key pairs.
***End-to-End Encryption:** Messages are encrypted with the recipient’s public key (using RSA with OAEP padding) and can only be decrypted with their corresponding private key.
***Command-Line Interface (CLI):** All interactions, from key generation to sending and receiving messages, are handled through a clean, text-based interface.
***Real-Time Communication:** A multi-threaded design allows users to send and receive messages simultaneously for a seamless, real-time chat experience.
***Modular & Documented Code:** The program is well-structured with clear, reusable functions and comprehensive comments for readability and maintenance.
***Graceful Error Handling:** The application is designed to manage common operational errors without crashing.