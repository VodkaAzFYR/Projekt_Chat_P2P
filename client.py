import socket
from cryptography.hazmat.primitives import serialization
from fun import generate_keys, decrypt_message, encrypt_message

private_key, public_key = generate_keys()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9050))

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
sock.sendall(pem)
server_public_key = serialization.load_pem_public_key(sock.recv(1024))

while True:
    message = input("Wpisz wiadomość: ")
    encrypted_message = encrypt_message(server_public_key, message)
    sock.sendall(encrypted_message)

    response = sock.recv(1024)
    print("Odpowiedź:", decrypt_message(private_key, response))

sock.close()
