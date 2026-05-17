import socket
import time

HOST = "127.0.0.1"
PORT = 5000

CHUNK_SIZE = 1024
BUFFER_SIZE = 1024

file_path = "files/input/test.txt"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq_num = 0

with open(file_path, "rb") as file:
    while True:
        chunk = file.read(CHUNK_SIZE)

        if not chunk:
            break

        packet = f"{seq_num}|".encode() + chunk

        client_socket.sendto(packet, (HOST, PORT))

        print(f"Paket gönderildi. Sequence: {seq_num}, Boyut: {len(chunk)} byte")

        ack, address = client_socket.recvfrom(BUFFER_SIZE)
        ack_text = ack.decode()

        print(f"ACK alındı: {ack_text}")

        seq_num += 1
        time.sleep(0.01)

client_socket.sendto(b"END", (HOST, PORT))

print("Dosya gönderimi tamamlandı.")
