import socket
import time

HOST = "127.0.0.1"
PORT = 5000
CHUNK_SIZE = 1024

file_path = "files/input/test.txt"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with open(file_path, "rb") as file:
    while True:
        chunk = file.read(CHUNK_SIZE)

        if not chunk:
            break

        client_socket.sendto(chunk, (HOST, PORT))
        print(f"Paket gönderildi: {len(chunk)} byte")
        time.sleep(0.01)

client_socket.sendto(b"END", (HOST, PORT))

print("Dosya gönderimi tamamlandı.")