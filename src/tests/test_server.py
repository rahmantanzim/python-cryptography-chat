from src.network.socket_handler import (
    create_server_socket,
    accept_client,
    send_packet,
    recv_packet,
)

def main():
    print("Starting test server on port 5000...")
    
    server_sock = create_server_socket(port=5000)
    print("Server is listening...")

    client_sock, addr = accept_client(server_sock)
    print(f"Client connected from: {addr}")

    # Receive message from client
    data = recv_packet(client_sock)
    print(f"Server received: {data!r}")

    # Send reply
    reply = b"Hello Tanzim"
    send_packet(client_sock, reply)
    print("Server sent reply.")

    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    main()
