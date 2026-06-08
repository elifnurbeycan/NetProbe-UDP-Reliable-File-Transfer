# NetProbe - UDP Tabanlı Güvenilir Dosya Aktarım Sistemi

## Proje Hakkında

NetProbe, UDP protokolü kullanılarak geliştirilen güvenilir dosya aktarım sistemidir.

UDP doğası gereği bağlantısız ve güvenilir olmayan bir protokoldür. Bu projede UDP üzerine Stop-and-Wait ARQ mekanizması uygulanarak güvenilir veri aktarımı sağlanmıştır.

Sistem;

- Dosyayı paketlere bölerek gönderir
- Her paket için ACK bekler
- ACK gelmezse timeout oluşur
- Paket yeniden gönderilir
- Aktarım sonunda SHA-256 ile dosya bütünlüğü doğrulanır

---

## Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|------------|------------|
| Python 3 | Uygulama geliştirme |
| UDP Socket | Veri iletimi |
| Stop-and-Wait ARQ | Güvenilir aktarım |
| SHA-256 | Dosya bütünlüğü doğrulama |
| Pandas | Veri analizi |
| Matplotlib | Grafik oluşturma |
| Wireshark | Paket analizi |
| Kali Linux | Test ortamı |

---

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
├── graphs/
│   ├── *_rtt_graph.png
│   ├── *_timeout_distribution.png
│   ├── retransmission_rate_comparison.png
│   ├── goodput_comparison.png
│   └── completion_time_comparison.png
│
└── README.md
```

---

## Sistem Mimarisi

```text
Client
   │
   ▼
UDP Packet
   │
   ▼
Server
   │
ACK
   │
   ▼
Client

Timeout oluşursa:
Client → Paketi yeniden gönderir
```

---

## Çalıştırma

### Sunucuyu Başlat

```bash
python3 server.py
```

### İstemciyi Başlat

```bash
python3 client.py
```

### Performans Analizi

```bash
python3 analysis.py
```

---

## Desteklenen Deney Senaryoları

NetProbe parametrik olarak tasarlanmıştır ve farklı ağ koşullarının sistem performansına etkisi analiz edilebilir.

| Parametre | Açıklama |
|------------|------------|
| ACK Kayıp Oranı (%) | ACK paketlerinin belirli oranlarda kaybedilmesi simüle edilir |
| Paket Boyutu | 512, 1024, 2048 byte gibi farklı paket boyutları test edilebilir |
| Dosya Boyutu | Küçük veya büyük dosyalarla aktarım performansı ölçülebilir |
| Timeout Değeri | Farklı timeout sürelerinin etkisi incelenebilir |
| Paket Sayısı | Farklı miktarda veri gönderilerek sistem yük altında test edilebilir |

---

## Ölçülen Performans Metrikleri

Her deney sonunda aşağıdaki metrikler hesaplanmaktadır.

| Metrik | Açıklama |
|---------|---------|
| RTT | Paket gönderimi ile ACK alınması arasındaki süre |
| Throughput | Birim zamanda iletilen toplam veri miktarı |
| Goodput | Başarıyla iletilen faydalı veri miktarı |
| Completion Time | Dosya aktarımının tamamlanma süresi |
| Timeout Count | Timeout oluşan paket sayısı |
| Retransmission Count | Yeniden gönderilen paket sayısı |
| Retransmission Rate | Yeniden gönderim oranı |
| SHA-256 Verification | Dosya bütünlüğü doğrulaması |

---

## Oluşturulan Grafikler

Proje analiz modülü otomatik olarak aşağıdaki grafikleri oluşturmaktadır.

### RTT Grafikleri

Her deney için paket bazında Round Trip Time değişimi gösterilir.

Örnek:

- loss0_rtt_graph.png
- loss10_rtt_graph.png
- loss20_rtt_graph.png
- loss30_rtt_graph.png
- chunk512_rtt_graph.png
- chunk2048_rtt_graph.png

---

### Timeout Dağılım Grafikleri

Başarılı paketler ile timeout oluşan paketlerin oranını gösterir.

Örnek:

- loss0_timeout_distribution.png
- loss10_timeout_distribution.png
- loss20_timeout_distribution.png
- loss30_timeout_distribution.png

---

### Retransmission Rate Karşılaştırması

Deneylerde oluşan yeniden gönderim oranlarının karşılaştırılması.

Dosya:

```text
retransmission_rate_comparison.png
```

---

### Goodput Karşılaştırması

Başarıyla iletilen faydalı veri miktarının karşılaştırılması.

Dosya:

```text
goodput_comparison.png
```

---

### Completion Time Karşılaştırması

Deneylerin tamamlanma sürelerinin karşılaştırılması.

Dosya:

```text
completion_time_comparison.png
```

---

## Wireshark Analizi

Proje sırasında Wireshark kullanılarak UDP paketleri incelenmiştir.

İncelenen başlıca çıktılar:

- UDP paket akışı
- ACK paketleri
- Flow Graph
- I/O Graph
- Packet Length Statistics
- Protocol Hierarchy Statistics

Bu analizler sayesinde paket kayıpları ve yeniden gönderimler doğrulanmıştır.

---

## Dosya Bütünlüğü Kontrolü

Aktarım tamamlandıktan sonra:

```text
Gönderilen Dosya SHA-256
=
Alınan Dosya SHA-256
```

karşılaştırması yapılmaktadır.

Hash değerlerinin eşit olması dosyanın hatasız aktarıldığını göstermektedir.

---

## Örnek Deneyler

Bu depoda aşağıdaki deneylere ait sonuçlar bulunmaktadır.

| Deney | Açıklama |
|---------|---------|
| loss0 | %0 ACK kaybı |
| loss10 | %10 ACK kaybı |
| loss20 | %20 ACK kaybı |
| loss30 | %30 ACK kaybı |
| chunk512 | 512 Byte paket boyutu |
| chunk2048 | 2048 Byte paket boyutu |

---

## Sonuç

Bu projede UDP üzerinde çalışan güvenilir bir dosya aktarım sistemi geliştirilmiştir.

Stop-and-Wait ARQ mekanizması sayesinde:

- Paket kayıpları tespit edilmiş
- Timeout yönetimi gerçekleştirilmiş
- Yeniden gönderim mekanizması uygulanmış
- Dosya bütünlüğü korunmuştur

Ayrıca performans analizi ve Wireshark incelemeleri ile sistem farklı ağ koşullarında değerlendirilmiştir.

---

**Bursa Teknik Üniversitesi**  
**Bilgisayar Ağları Dersi Projesi**
**Elif Nur Beycan 24360859210**
**Kübra Kaya 23360859736**
**Ceren Ebrar Yücetombullar 22360859010**
**2025-2026**
