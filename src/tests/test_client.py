from src.network.socket_handler import (
    create_client_socket,
    send_packet,
    recv_packet,
)


def main():
    print("Connecting to server...")
    sock = create_client_socket("127.0.0.1", 5000)

    # Send message
    msg = b"Hello Tanzim Rahman"
    send_packet(sock, msg)
    print(f"Client sent: {msg!r}")

    # Receive reply
    reply = recv_packet(sock)
    print(f"Client received: {reply!r}")

    sock.close()


if __name__ == "__main__":
    main()
