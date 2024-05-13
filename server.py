import socket
from cryptography.hazmat.primitives import serialization
from fun import generate_keys, decrypt_message, encrypt_message

def run_server():
    host = 'localhost'
    port = 9050
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print("Serwer nasłuchuje na porcie", port)

    while True:
        conn, addr = server.accept()
        print('Połączono z:', addr)

        client_public_key = serialization.load_pem_public_key(conn.recv(1024))

        private_key, public_key = generate_keys()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        conn.sendall(pem)

        while True:
            encrypted_msg = conn.recv(1024)
            if not encrypted_msg:
                break
            print("Otrzymano zaszyfrowaną wiadomość")

            message = decrypt_message(private_key, encrypted_msg)
            print("Wiadomość:", message)

            response = encrypt_message(client_public_key, 'Odebrano: ' + message)
            conn.sendall(response)

        conn.close()

if __name__ == '__main__':
    run_server()