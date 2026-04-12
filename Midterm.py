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
        client_socket.sendall(b"Hello! You are connected to the server. Type 'exit' to disconnect.\n")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Client {client_address[0]}:{client_address[1]} disconnected.")
                    break
                message = data.decode('utf-8', errors='ignore').strip()
                print(f"Received from client: {message}")
                if message.lower() == 'exit':
                    client_socket.sendall(b"Goodbye!\n")
                    print(f"Client {client_address[0]}:{client_address[1]} requested disconnect.")
                    break
                client_socket.sendall(b"Echo: " + data + b"\n")
        finally:
            client_socket.close()
