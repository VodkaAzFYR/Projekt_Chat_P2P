# server.py

import socket
import threading
from fun import decrypt_message
from load_keys import load_private_key

def handle_client(client_socket, private_key):
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        decrypted_message = decrypt_message(private_key, data)
        print(f"Received: {decrypted_message}")
        response = input("Reply: ")
        client_socket.sendall(response.encode())  # No encryption here
    client_socket.close()

def server(private_key_path):
    private_key = load_private_key(private_key_path)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, private_key))
        client_handler.start()

if __name__ == "__main__":
    private_key_path = "private_key.pem"
    server(private_key_path)
