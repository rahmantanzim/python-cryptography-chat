"""
This module is for Socket handling. 
Objectives: 
    - Create server and client TCP sockets
"""

import socket
import struct
from typing import Optional, Tuple

# 4-byte big-endian unsigned int for message length
_HEADER_SIZE = 4
_DEFAULT_BACKLOG = 1  # only one peer needed for this chat

def create_server_socket(host: str = '0.0.0.0', port: int = 5000) ->socket.socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates a new IPv4 TCP socket
    server_sock.setsockopt(socket.SOCK_SEQPACKET, socket.SO_REUSEADDR,1) #Allow reusing the same port after a restart
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
    if timeout is not None:
        client_sock.settimeout(timeout)
    try:
        client_sock.connect((server_host, server_port))
        client_sock.settimeout(None)
        return client_sock # connected socket
    except Exception:
        client_sock.close() #If connection fails, the socket is closed properly
        raise
    
