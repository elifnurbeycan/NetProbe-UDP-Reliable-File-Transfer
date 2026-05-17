import pandas as pd

log_path = "logs/transfer_log.csv"

df = pd.read_csv(log_path)

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
