import socket
import os
import hashlib

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 2048

os.makedirs("files/received", exist_ok=True)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Server listening on {HOST}:{PORT}")

received_file_path = "files/received/received_test.txt"

received_packets = set()
dropped_ack = False

def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()

with open(received_file_path, "wb") as file:

    while True:

        data, address = server_socket.recvfrom(BUFFER_SIZE)

        if data == b"END":
            print("Dosya aktarımı tamamlandı.")
            break

        header, chunk = data.split(b"|", 1)

        seq_num = int(header.decode())

        print(f"Paket alındı. Sequence: {seq_num}, Boyut: {len(chunk)} byte")

        if seq_num in received_packets:

            print(f"Duplicate paket tespit edildi. Sequence: {seq_num}. Dosyaya tekrar yazılmadı.")

            ack_message = f"ACK|{seq_num}"

            server_socket.sendto(ack_message.encode(), address)

            print(f"ACK tekrar gönderildi: {ack_message}")

            continue

        received_packets.add(seq_num)

        if seq_num == 0 and not dropped_ack:

            print("TEST: ACK bilerek gönderilmedi.")

            dropped_ack = True

            continue

        file.write(chunk)

        ack_message = f"ACK|{seq_num}"

        server_socket.sendto(ack_message.encode(), address)

        print(f"ACK gönderildi: {ack_message}")

received_hash = calculate_sha256(received_file_path)

print(f"Alınan dosya SHA-256: {received_hash}")

print(f"Dosya kaydedildi: {received_file_path}")
