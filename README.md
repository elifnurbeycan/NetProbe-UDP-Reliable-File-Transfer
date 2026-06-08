# NetProbe

Bilgisayar Ağları dersi kapsamında geliştirilen NetProbe, UDP protokolü üzerinde güvenilir dosya aktarımı gerçekleştiren ve ağ performansını analiz eden bir uygulamadır.

## Proje Özeti

UDP doğası gereği paket teslim garantisi sağlamaz. Bu projede UDP üzerine;

- Sequence Number
- ACK (Onay) Mekanizması
- Timeout Kontrolü
- Retransmission (Yeniden Gönderim)
- SHA-256 Bütünlük Doğrulaması

mekanizmaları eklenerek güvenilir dosya aktarımı sağlanmıştır.

## Kullanılan Teknolojiler

- Python 3
- UDP Socket Programlama
- SHA-256 Hash Algoritması
- Pandas
- Matplotlib
- Wireshark
- Kali Linux (VMware)
- Visual Studio Code

## Proje Yapısı

```text
NetProbe/
│
├── client.py
├── server.py
├── analysis.py
│
├── files/
│   ├── input/
│   └── received/
│
├── logs/
│   ├── transfer_log.csv
│   ├── experiment_results.csv
│   └── experiment_summary.csv
│
└── graphs/
```

## Çalıştırma

### Sunucuyu Başlat

```bash
python3 server.py
```

### İstemciyi Başlat

```bash
python3 client.py
```

### Analizleri Oluştur

```bash
python3 analysis.py
```

## Gerçekleştirilen Deneyler

### Senaryo 1 - ACK Kayıp Oranı Analizi

- %0 ACK kaybı
- %10 ACK kaybı
- %20 ACK kaybı
- %30 ACK kaybı

İncelenen metrikler:

- RTT
- Throughput
- Goodput
- Completion Time
- Retransmission Rate

### Senaryo 2 - Paket Boyutu Analizi

- 512 Byte
- 1024 Byte
- 2048 Byte

İncelenen metrikler:

- RTT
- Throughput
- Goodput
- Completion Time
- Retransmission Rate

## Özellikler

- Güvenilir UDP dosya aktarımı
- ACK tabanlı kontrol mekanizması
- Timeout yönetimi
- Otomatik yeniden gönderim
- Çift paket kontrolü
- SHA-256 bütünlük doğrulaması
- RTT hesaplama
- Throughput ve Goodput analizi
- CSV loglama
- Otomatik grafik üretimi
- Wireshark ile trafik analizi

## Proje Ekibi

- Elif Nur Beycan
- Kübra Kaya
- Ceren Ebrar Yücetombullar

Bursa Teknik Üniversitesi  
Bilgisayar Mühendisliği Bölümü  
Bilgisayar Ağları Dönem Projesi - 2026
