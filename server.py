import socket
import os

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 2048

os.makedirs("files/received", exist_ok=True)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Server listening on {HOST}:{PORT}")

received_file_path = "files/received/received_test.txt"

with open(received_file_path, "wb") as file:
    while True:
        data, address = server_socket.recvfrom(BUFFER_SIZE)

        if data == b"END":
            print("Dosya aktarımı tamamlandı.")
            break

        header, chunk = data.split(b"|", 1)
        seq_num = int(header.decode())

        file.write(chunk)

        ack_message = f"ACK|{seq_num}"
        server_socket.sendto(ack_message.encode(), address)

        print(f"Paket alındı. Sequence: {seq_num}, Boyut: {len(chunk)} byte")

print(f"Dosya kaydedildi: {received_file_path}")
