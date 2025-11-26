import socket
import threading
from typing import Optional

from src.network import socket_handler as sh
from src.security import key_manager as km

def _load_keys(path_public_key_of_partner:str):
    #Loads private key and public key of partner from key_manager module
    try:
        private_key = km.load_private_key()
        
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        print(f"Solution hint: ")
        return None,None
    try:
        public_key_of_partner = km.load_public_key(path_public_key_of_partner)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        print(f"Solution hint: ")
        return None,None
    return private_key, public_key_of_partner

def _receive_loop(sock:socket.socket, private_key, stop_event: threading.Event,role_label: str)-> None:
    #look for incoming encrypted messages in a loop
    # decrypt them
    while not stop_event.is_set():
        try:
            packet = sh.recv_packet(sock)
            if packet is None:
                print("\n [MESSAGE] Peer Disconnected")
                stop_event.set()
                break
            try:
                message = km.decrypt_message(packet, private_key)
            except ValueError as exc:
                print(f"\n[WARNING] Message decryption failed: {exc}")
                continue
            print(f"\n[{role_label} PEER] {message}")
            print("> ", end="", flush=True)    
        except OSError as exc:
            if not stop_event.is_set():
                print(f"\n[ERROR] Socket error in receive loop: {exc}")
                stop_event.set()
            break

def _chat_loop(sock:socket.socket, private_key,public_key_of_partner, role_label:str)-> None:
    stop_event = threading.Event() 
    # make a new thread separete from main app
    receiver_thread = threading.Thread(
        target=_receive_loop,
        args = (sock,private_key,stop_event,role_label),
        daemon=True
    )
    
            
    
