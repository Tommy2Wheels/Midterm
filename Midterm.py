import socket

HOST = '127.0.0.1'  # Listen on all interfaces
PORT = 8080       # You can change this to any port > 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address[0]}:{client_address[1]}")
        client_socket.sendall(b"Hello! You are connected to the server.\n")
        client_socket.close()
