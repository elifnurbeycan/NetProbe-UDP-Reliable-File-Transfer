---

## Desteklenen Deney Senaryoları

NetProbe farklı ağ koşullarının performans üzerindeki etkisini incelemek amacıyla parametrik olarak tasarlanmıştır.

Aşağıdaki deneyler gerçekleştirilebilir:

| Parametre | Açıklama |
|------------|------------|
| ACK Kayıp Oranı (%) | Sunucu tarafında ACK paketlerinin belirli bir oranla kaybedilmesi simüle edilir. |
| Paket Boyutu (Chunk Size) | 512, 1024, 2048 byte gibi farklı paket boyutlarının performansa etkisi ölçülür. |
| Dosya Boyutu | Küçük veya büyük dosyalar kullanılarak aktarım süresi ve verimlilik karşılaştırılır. |
| Timeout Değeri | Timeout süresi değiştirilerek yeniden gönderim davranışı incelenir. |
| Gönderilen Paket Sayısı | Test verisi miktarı değiştirilerek sistem yük altında test edilir. |

---

## Ölçülen Performans Metrikleri

Her deney sonunda aşağıdaki performans değerleri hesaplanmaktadır:

| Metrik | Açıklama |
|---------|---------|
| RTT | Paket gönderimi ile ACK alınması arasındaki süre |
| Throughput | Birim zamanda iletilen toplam veri miktarı |
| Goodput | Başarıyla iletilen faydalı veri miktarı |
| Completion Time | Dosya aktarımının tamamlanma süresi |
| Timeout Count | Timeout oluşan paket sayısı |
| Retransmission Count | Yeniden gönderilen paket sayısı |
| Retransmission Rate | Yeniden gönderim oranı |
| SHA-256 Verification | Dosya bütünlük doğrulaması |

---

## Bu Depoda Yer Alan Örnek Sonuçlar

Bu depodaki grafikler aşağıdaki deneylerden elde edilmiştir:

| Deney | Değiştirilen Parametre |
|--------|--------|
| loss0 | %0 ACK kaybı |
| loss10 | %10 ACK kaybı |
| loss20 | %20 ACK kaybı |
| loss30 | %30 ACK kaybı |
| chunk512 | 512 Byte paket boyutu |
| chunk2048 | 2048 Byte paket boyutu |

Sistem farklı dosya boyutları, timeout değerleri ve paket boyutları ile de test edilebilecek şekilde tasarlanmıştır.
