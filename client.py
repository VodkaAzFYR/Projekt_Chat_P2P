# client.py

from fun import encrypt_message, connect_to_tor
from load_keys import load_public_key

def client(public_key_path, server_address):
    public_key = load_public_key(public_key_path)
    client_socket = connect_to_tor(server_address, 12345)

    while True:
        message = input("Message: ")
        encrypted_message = encrypt_message(public_key, message)
        client_socket.sendall(encrypted_message)
        response = client_socket.recv(4096)
        if response:
            print(f"Received: {response.decode()}")  # No decryption here

    client_socket.close()

if __name__ == "__main__":
    public_key_path = "public_key.pem"
    server_address = "your_tor_onion_address"
    client(public_key_path, server_address)
