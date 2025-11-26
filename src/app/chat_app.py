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
        args = (sock,private_key,stop_event,role_label), #calls receive_loop() with args as arguments
        daemon=True #if programm stops, thread ends 
    )
    receiver_thread.start()
    
    print(f"Connected as {role_label}.")
    print("Type your messages and press Enter to send.")
    print("Type '/quit' or '/exit' to close the chat.")

    while not stop_event.is_set():
        try:
            user_input = input("> ")
        except EOFError: #if user types ctrl+D
            user_input = "/quit"
        
        if user_input.strip().lower() in ("/quit", "exit"):
            stop_event.set()
            break
        
        if user_input == '':
            continue #skipping empty message
            
        try:
            crypto_text = km.encrypt_message(user_input,public_key_of_partner)
            sh.send_packet(sock,crypto_text)
        except Exception as exc:
            print(f"[ERROR] Failed to send message: {exc}")
            stop_event.set()
            break
               
    # Lastly, lets shutdown the socket
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except:
        pass
    sock.close()

    print("Chat is closed.")


#Start the app as Server
def start_server(port:int,path_public_key_of_partner: str, host:str = '0.0.0.0')->None:
    print(f"[SERVER] Starting on {host}:{port} ...")
    try:
        server_sock = sh.create_server_socket(host=host, port=port)
    except OSError as exc:
        print(f"[ERROR] Failed to start server socket: {exc}")
        return

    print("[SERVER] Waiting for a client to connect...")
    try:
        client_sock, addr = sh.accept_client(server_sock)
    except OSError as exc:
        print(f"[ERROR] Failed to accept client: {exc}")
        server_sock.close()
        return

    print(f"[SERVER] Client connected from {addr[0]}:{addr[1]}")
    server_sock.close()
        
    private_key,public_key_of_partner = _load_keys(path_public_key_of_partner)
    if private_key is None or public_key_of_partner is None:
        client_sock.close()
        return
    
    _chat_loop(client_sock, private_key, public_key_of_partner, role_label="SERVER")

#Start the app as Client    
def start_client(
    server_host:str,
    port:int,
    path_public_key_of_partner: str,
):
    print(f"[CLIENT] Connecting to {server_host}:{port} ...")
    
    try: 
        sock = sh.create_client_socket(server_host, port) 
    except Exception as exc:
        print(f"[ERROR] could not connect to server: {exc}")
        return
    
    print("[Client] is connected with the Server")
    
    private_key, public_key_partner = _load_keys(path_public_key_of_partner)
    if private_key is None or public_key_partner is None:
        sock.close()
        return

    _chat_loop(sock, private_key, public_key_partner, role_label="CLIENT")