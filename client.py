import socket
import time
import hashlib
import csv
import os

HOST = "127.0.0.1"
PORT = 5000

CHUNK_SIZE = 1024
BUFFER_SIZE = 1024

TIMEOUT = 1.0
MAX_RETRIES = 5

file_path = "files/input/test.txt"
log_path = "logs/transfer_log.csv"

os.makedirs("logs", exist_ok=True)
os.makedirs("files/input", exist_ok=True)

data_count = int(input("Kaç adet test verisi oluşturulsun?: "))

with open(file_path, "w") as file:
    for i in range(1, data_count + 1):
        file.write(f"NETPROBE TEST DATA {i}\n")

print(f"{data_count} adet test verisi oluşturuldu: {file_path}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()

original_hash = calculate_sha256(file_path)
print(f"Orijinal dosya SHA-256: {original_hash}")

with open(log_path, "w", newline="") as log_file:
    writer = csv.writer(log_file)

    writer.writerow([
        "sequence_number",
        "send_time",
        "ack_time",
        "rtt",
        "attempt",
        "timeout",
        "status"
    ])

    seq_num = 0
    transfer_start = time.time()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)

            if not chunk:
                break

            packet = f"{seq_num}|".encode() + chunk

            retries = 0
            ack_received = False

            while retries < MAX_RETRIES and not ack_received:
                send_time = time.time()

                client_socket.sendto(packet, (HOST, PORT))
                print(f"Paket gönderildi. Sequence: {seq_num}, Deneme: {retries + 1}")

                try:
                    ack, address = client_socket.recvfrom(BUFFER_SIZE)

                    ack_time = time.time()
                    rtt = ack_time - send_time
                    ack_text = ack.decode()

                    if ack_text == f"ACK|{seq_num}":
                        print(f"ACK alındı: {ack_text}")

                        writer.writerow([
                            seq_num,
                            send_time,
                            ack_time,
                            rtt,
                            retries + 1,
                            "No",
                            "ACK_RECEIVED"
                        ])

                        ack_received = True

                except socket.timeout:
                    retries += 1

                    print(f"Timeout oluştu. Sequence {seq_num} tekrar gönderilecek.")

                    writer.writerow([
                        seq_num,
                        send_time,
                        "",
                        "",
                        retries,
                        "Yes",
                        "TIMEOUT"
                    ])

            if not ack_received:
                print("Maksimum yeniden gönderim sayısına ulaşıldı.")

                writer.writerow([
                    seq_num,
                    "",
                    "",
                    "",
                    retries,
                    "Yes",
                    "FAILED"
                ])

                break

            seq_num += 1
            time.sleep(0.01)

    transfer_end = time.time()

client_socket.sendto(b"END", (HOST, PORT))

print("Dosya gönderimi tamamlandı.")
print(f"Toplam aktarım süresi: {transfer_end - transfer_start:.4f} saniye")
print(f"Log dosyası oluşturuldu: {log_path}")
