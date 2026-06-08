import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

log_path = "logs/transfer_log.csv"
experiment_path = "logs/experiment_results.csv"
summary_path = "logs/experiment_summary.csv"

os.makedirs("graphs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

df = pd.read_csv(log_path)

total_packets = df["sequence_number"].nunique()
total_attempts = len(df)

timeout_count = len(df[df["timeout"] == "Yes"])
successful_acks = len(df[df["status"] == "ACK_RECEIVED"])

retransmission_count = total_attempts - total_packets
retransmission_rate = retransmission_count / total_attempts if total_attempts > 0 else 0

valid_rtt = df["rtt"].dropna()
average_rtt = valid_rtt.mean() if len(valid_rtt) > 0 else 0

completion_time = df["ack_time"].max() - df["send_time"].min()

file_size = df["file_size"].dropna().iloc[0]
chunk_size = df["chunk_size"].dropna().iloc[0]
timeout_value = df["timeout_value"].dropna().iloc[0]

if completion_time > 0:
    goodput = file_size / completion_time
    throughput = (total_attempts * chunk_size) / completion_time
else:
    goodput = 0
    throughput = 0

print("=== NetProbe Performans Analizi ===")
print(f"Dosya boyutu: {file_size} byte")
print(f"Paket boyutu: {chunk_size} byte")
print(f"Timeout değeri: {timeout_value} saniye")
print(f"Toplam paket sayısı: {total_packets}")
print(f"Toplam gönderim denemesi: {total_attempts}")
print(f"Başarılı ACK sayısı: {successful_acks}")
print(f"Timeout sayısı: {timeout_count}")
print(f"Retransmission sayısı: {retransmission_count}")
print(f"Retransmission rate: {retransmission_rate:.2f}")
print(f"Ortalama RTT: {average_rtt:.6f} saniye")
print(f"Completion time: {completion_time:.6f} saniye")
print(f"Throughput: {throughput:.2f} byte/s")
print(f"Goodput: {goodput:.2f} byte/s")

save_experiment = input("Bu deney sonucunu kaydetmek ister misiniz? (e/h): ")

experiment_name = "default"

if save_experiment.lower() == "e":
    experiment_name = input("Deney adı giriniz: ")
    loss_rate = input("ACK kayıp oranı (%) giriniz: ")
else:
    experiment_name = input("Grafik dosya adı için deney adı giriniz: ")
    loss_rate = ""

safe_experiment_name = experiment_name.replace(" ", "_").replace("/", "_")

# Deneye özel RTT grafiği
plt.figure(figsize=(8, 5))
plt.plot(
    df[df["status"] == "ACK_RECEIVED"]["sequence_number"],
    df[df["status"] == "ACK_RECEIVED"]["rtt"],
    marker="o"
)
plt.xlabel("Sequence Number")
plt.ylabel("RTT (saniye)")
plt.title(f"RTT Değerleri - {experiment_name}")
plt.grid(True)
plt.tight_layout()

rtt_graph_path = f"graphs/{safe_experiment_name}_rtt_graph.png"
plt.savefig(rtt_graph_path)
print(f"RTT grafiği oluşturuldu: {rtt_graph_path}")

# Deneye özel timeout dağılımı grafiği
timeout_data = [
    len(df[df["timeout"] == "Yes"]),
    len(df[df["timeout"] == "No"])
]

labels = ["Timeout", "Başarılı"]

plt.figure(figsize=(6, 6))
plt.pie(timeout_data, labels=labels, autopct="%1.1f%%")
plt.title(f"Timeout Dağılımı - {experiment_name}")
plt.tight_layout()

timeout_graph_path = f"graphs/{safe_experiment_name}_timeout_distribution.png"
plt.savefig(timeout_graph_path)
print(f"Timeout grafiği oluşturuldu: {timeout_graph_path}")

if save_experiment.lower() == "e":
    experiment_file_exists = os.path.exists(experiment_path)
    summary_file_exists = os.path.exists(summary_path)

    with open(experiment_path, "a", newline="") as file:
        writer = csv.writer(file)

        if not experiment_file_exists:
            writer.writerow([
                "experiment_name",
                "loss_rate",
                "file_size",
                "chunk_size",
                "timeout_value",
                "total_packets",
                "total_attempts",
                "successful_acks",
                "timeout_count",
                "retransmission_count",
                "retransmission_rate",
                "average_rtt",
                "completion_time",
                "throughput",
                "goodput",
                "rtt_graph",
                "timeout_graph"
            ])

        writer.writerow([
            experiment_name,
            loss_rate,
            file_size,
            chunk_size,
            timeout_value,
            total_packets,
            total_attempts,
            successful_acks,
            timeout_count,
            retransmission_count,
            retransmission_rate,
            average_rtt,
            completion_time,
            throughput,
            goodput,
            rtt_graph_path,
            timeout_graph_path
        ])

    with open(summary_path, "a", newline="") as file:
        writer = csv.writer(file)

        if not summary_file_exists:
            writer.writerow([
                "Deney",
                "ACK Kayip Orani (%)",
                "Dosya Boyutu (byte)",
                "Paket Boyutu (byte)",
                "Timeout (s)",
                "Toplam Paket",
                "Timeout Sayisi",
                "Retransmission Rate",
                "Ortalama RTT (s)",
                "Completion Time (s)",
                "Throughput (byte/s)",
                "Goodput (byte/s)"
            ])

        writer.writerow([
            experiment_name,
            loss_rate,
            int(file_size),
            int(chunk_size),
            timeout_value,
            total_packets,
            timeout_count,
            round(retransmission_rate, 4),
            round(average_rtt, 6),
            round(completion_time, 6),
            round(throughput, 2),
            round(goodput, 2)
        ])

    print(f"Detaylı deney sonucu kaydedildi: {experiment_path}")
    print(f"Rapor için özet tablo kaydedildi: {summary_path}")

# Deney karşılaştırma grafikleri
if os.path.exists(experiment_path):
    try:
        exp_df = pd.read_csv(experiment_path)
    except Exception:
        print("Eski veya bozuk deney dosyası tespit edildi.")
        print("Yeni deney dosyası oluşturmak için eski dosya siliniyor.")
        os.remove(experiment_path)
        exp_df = pd.DataFrame()

    if not exp_df.empty and len(exp_df) >= 2:
        plt.figure(figsize=(9, 5))
        plt.bar(exp_df["experiment_name"], exp_df["completion_time"])
        plt.xlabel("Deney")
        plt.ylabel("Completion Time (saniye)")
        plt.title("Deneylere Göre Completion Time Karşılaştırması")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig("graphs/completion_time_comparison.png")
        print("Completion time karşılaştırma grafiği oluşturuldu: graphs/completion_time_comparison.png")

        plt.figure(figsize=(9, 5))
        plt.bar(exp_df["experiment_name"], exp_df["retransmission_rate"])
        plt.xlabel("Deney")
        plt.ylabel("Retransmission Rate")
        plt.title("Deneylere Göre Retransmission Rate Karşılaştırması")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig("graphs/retransmission_rate_comparison.png")
        print("Retransmission rate karşılaştırma grafiği oluşturuldu: graphs/retransmission_rate_comparison.png")

        plt.figure(figsize=(9, 5))
        plt.bar(exp_df["experiment_name"], exp_df["goodput"])
        plt.xlabel("Deney")
        plt.ylabel("Goodput (byte/s)")
        plt.title("Deneylere Göre Goodput Karşılaştırması")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig("graphs/goodput_comparison.png")
        print("Goodput karşılaştırma grafiği oluşturuldu: graphs/goodput_comparison.png")
    else:
        print("Karşılaştırma grafiği için en az 2 deney sonucu gereklidir.")
