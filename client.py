import socket
import time

HOST = "127.0.0.1"
PORT = 5000

CHUNK_SIZE = 1024
BUFFER_SIZE = 1024

TIMEOUT = 1.0
MAX_RETRIES = 5

file_path = "files/input/test.txt"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

seq_num = 0

with open(file_path, "rb") as file:
    while True:
        chunk = file.read(CHUNK_SIZE)

        if not chunk:
            break

        packet = f"{seq_num}|".encode() + chunk

        retries = 0
        ack_received = False

        while retries < MAX_RETRIES and not ack_received:

            client_socket.sendto(packet, (HOST, PORT))

            print(f"Paket gönderildi. Sequence: {seq_num}, Deneme: {retries + 1}")

            try:
                ack, address = client_socket.recvfrom(BUFFER_SIZE)

                ack_text = ack.decode()

                if ack_text == f"ACK|{seq_num}":
                    print(f"ACK alındı: {ack_text}")
                    ack_received = True

            except socket.timeout:
                retries += 1
                print(f"Timeout oluştu. Sequence {seq_num} tekrar gönderilecek.")

        if not ack_received:
            print("Maksimum yeniden gönderim sayısına ulaşıldı.")
            break

        seq_num += 1
        time.sleep(0.01)

client_socket.sendto(b"END", (HOST, PORT))

print("Dosya gönderimi tamamlandı.")
