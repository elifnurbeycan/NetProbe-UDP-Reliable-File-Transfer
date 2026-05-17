import pandas as pd
import matplotlib.pyplot as plt
import os

log_path = "logs/transfer_log.csv"

df = pd.read_csv(log_path)

os.makedirs("graphs", exist_ok=True)

total_packets = df["sequence_number"].nunique()
total_attempts = len(df)

timeout_count = len(df[df["timeout"] == "Yes"])

successful_acks = len(df[df["status"] == "ACK_RECEIVED"])

retransmission_count = total_attempts - total_packets

if total_attempts > 0:
    retransmission_rate = retransmission_count / total_attempts
else:
    retransmission_rate = 0

valid_rtt = df["rtt"].dropna()

if len(valid_rtt) > 0:
    average_rtt = valid_rtt.mean()
else:
    average_rtt = 0

completion_time = df["ack_time"].max() - df["send_time"].min()

print("=== NetProbe Performans Analizi ===")
print(f"Toplam paket sayısı: {total_packets}")
print(f"Toplam gönderim denemesi: {total_attempts}")
print(f"Başarılı ACK sayısı: {successful_acks}")
print(f"Timeout sayısı: {timeout_count}")
print(f"Retransmission sayısı: {retransmission_count}")
print(f"Retransmission rate: {retransmission_rate:.2f}")
print(f"Ortalama RTT: {average_rtt:.6f} saniye")
print(f"Completion time: {completion_time:.6f} saniye")

# RTT grafiği

plt.figure(figsize=(8, 5))

plt.plot(
    df[df["status"] == "ACK_RECEIVED"]["sequence_number"],
    df[df["status"] == "ACK_RECEIVED"]["rtt"],
    marker="o"
)

plt.xlabel("Sequence Number")
plt.ylabel("RTT (saniye)")
plt.title("RTT Değerleri")

plt.grid(True)

plt.savefig("graphs/rtt_graph.png")

print("RTT grafiği oluşturuldu: graphs/rtt_graph.png")

# Timeout grafiği

timeout_data = [
    len(df[df["timeout"] == "Yes"]),
    len(df[df["timeout"] == "No"])
]

labels = ["Timeout", "Başarılı"]

plt.figure(figsize=(6, 6))

plt.pie(timeout_data, labels=labels, autopct='%1.1f%%')

plt.title("Timeout Dağılımı")

plt.savefig("graphs/timeout_distribution.png")

print("Timeout grafiği oluşturuldu: graphs/timeout_distribution.png")
