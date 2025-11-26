"""
This module is for Socket handling. 
Objectives: 
    - Create server and client TCP sockets
List of functions:
********************
create_server_socket()
create_client_socket()
accept_client()
_recv_exact() #helper function
send_packet()
recv_packet()

"""

import socket
import struct
from typing import Optional, Tuple

# 4-byte big-endian unsigned int for message length
_HEADER_SIZE = 4
_DEFAULT_BACKLOG = 1  # only one peer needed for this chat

def create_server_socket(host: str = '0.0.0.0', port: int = 5000) ->socket.socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates a new IPv4 TCP socket
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #Allow reusing the same port after a restart
    server_sock.bind((host,port))
    server_sock.listen(_DEFAULT_BACKLOG) #Allow one waiting client at most
    return server_sock

def accept_client(server_sock: socket.socket) -> Tuple[socket.socket, Tuple[str, int]]:
    client_sock,addr = server_sock.accept() #wait until a client connects
    return client_sock,addr

def create_client_socket(
    server_host:str,
    server_port: int,
    timeout: Optional[float] = 10.0    
)->socket.socket:
    # Goal is to create a TCP cleint socket and connect to the server.
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates a new IPv4 TCP socket
    if timeout is not None: # safety check
        client_sock.settimeout(timeout)
    try:
        client_sock.connect((server_host, server_port))
        client_sock.settimeout(None)
        return client_sock # connected socket
    except Exception:
        client_sock.close() #If connection fails, the socket is closed properly
        raise
    
def _recv_exact(sock: socket.socket, num_bytes: int) -> Optional[bytes]:
    chunks = []
    remaining = num_bytes

    while remaining > 0:
        chunk = sock.recv(remaining) #call for all remaining bytes
        if chunk == b"":  # empty byte === closed connection
            return None
        chunks.append(chunk)
        remaining -= len(chunk)

    return b"".join(chunks)

def send_packet(sock: socket.socket, data: bytes)-> None:
    if not isinstance(data,(bytes,bytearray)):
        raise TypeError('Data must be in bytes ')
    length = len(data) #length will be stored in a 4-byte header
    # building the '4-byte header'
    header = struct.pack("!I",length) # ! = network byte order, I = unsigned integer
    sock.sendall(header+data) # keeps sending all the bytes of the data
    
def recv_packet(sock:socket.socket)-> Optional[bytes]:
    header = _recv_exact(sock, _HEADER_SIZE)   
    if header is None:
        return None
    (length,) = struct.unpack("!I", header)
    
    if length < 0 :
        raise ValueError("Invalid packet length")
    
    if length == 0:
        return b"" 
    data = _recv_exact(sock,length)
    
    return data