# 🤖 DAO Akıllı Sağlık ve Aktivite Paneli (API Katmanı)

Bu proje; akıllı saatler, bileklikler ve mobil uygulamalardan gelen günlük sağlık ve aktivite verilerini (adım sayısı, trendler vb.) otonom olarak işleyen, analiz eden ve bulut-yerel hibrit yapay zeka mimarisiyle kullanıcıya kişiselleştirilmiş sağlık mentorluğu sunan **üretim standartlarında (Production-Ready) bir FastAPI Backend** uygulamasıdır.

---

## 🏗️ Sistem Mimarisi & Veri Akışı

Sistem, gelen verilerin güvenliğini ve analitik doğruluğunu sağlamak amacıyla **Repository → Service → Controller** mimarisi prensiplerine uygun olarak tasarlanmıştır.

```text
[Akıllı Saat / Mobil Uygulama]
                │
                │ JSON POST /api/steps
                ▼
        [FastAPI Gateway]
                │
                ▼
    [Pydantic Veri Doğrulama]
                │
      ┌─────────┴─────────┐
      │                   │
      ▼                   ▼
[SQLite Veri Katmanı]  [NumPy Analitik Motoru]
(Kalıcı Hafıza)        (Trend & DAO Score)
      │                   │
      └─────────┬─────────┘
                ▼
         [Hibrit LLM Katmanı]
                │
      ┌─────────┴─────────┐
      │                   │
      ▼                   ▼
 [Google Gemini API]  [Gemma 2 2B-IT]
 (Bulut Motoru)       (Yerel Yedek Motor)
                │
                ▼
     [Dashboard JSON Yanıtı]
         GET /api/dashboard
```

---

## 🌟 Öne Çıkan Özellikler

### ⚡ Hibrit LLM Stratejisi (Failover)

Yapay zeka koçluğu talepleri öncelikli olarak yüksek hızlı bulut tabanlı **Gemini API** üzerinden yürütülür.

* Ortalama yanıt süresi: **1–2 saniye**
* API kotası dolduğunda veya internet bağlantısı kesildiğinde otomatik geçiş
* Yerel çalışan **Gemma 2 (2B-IT)** modeli ile kesintisiz hizmet

### 🎯 Gelişmiş Analitik Motoru

Sistem yalnızca veri depolamakla kalmaz.

NumPy destekli analiz motoru sayesinde:

* Haftalık ortalama hesaplama
* Standart sapma analizi
* Aktivite istikrar ölçümü
* Trend tespiti
* DAO Sağlık Skoru üretimi (0–100)

### 📦 %100 Taşınabilir (Dockerized)

Docker desteği sayesinde uygulama aşağıdaki ortamlarda kolayca çalıştırılabilir:

* Render
* Railway
* AWS
* Azure
* Google Cloud
* Docker destekli tüm Linux sunucuları

### 🛡️ Güçlü Veri Doğrulama

Pydantic modelleri sayesinde:

* Eksik veri paketleri reddedilir
* Hatalı veri tipleri engellenir
* API katmanında otomatik validasyon sağlanır

---

## 📂 Proje Yapısı

```text
dao-health-backend/
│
├── main_v2.py
│   └── API endpointleri ve Hibrit LLM yönetimi
│
├── activity_rings.py
│   └── Akıllı saat aktivite halkaları için HTML/SVG motoru
│
├── requirements.txt
│   └── Gerekli Python bağımlılıkları
│
├── Dockerfile
│   └── Container yapılandırması
│
└── ajan_hafizasi.db
    └── SQLite veritabanı
```

---

# 🛠️ API Endpoints

Sunucu çalıştırıldıktan sonra Swagger arayüzüne aşağıdaki adresten erişilebilir:

```text
http://localhost:8000/docs
```

---

## 🔍 Sistem Sağlık Kontrolü

### Endpoint

```http
GET /
```

### Açıklama

API sunucusunun aktif olup olmadığını doğrular.

### Örnek Yanıt

```json
{
  "status": "online",
  "message": "DAO Akıllı Sağlık Ajanı API Katmanı V2 Aktif!"
}
```

---

## 🚶 Adım Verisi Kaydetme

### Endpoint

```http
POST /api/steps
```

### Açıklama

Akıllı saat veya mobil uygulama tarafından günlük adım verilerini sisteme kaydeder.

### İstek Gövdesi

```json
{
  "gun_adi": "Cumartesi",
  "adim_sayisi": 12500
}
```

---

## 📊 Dashboard Verisi Alma

### Endpoint

```http
GET /api/dashboard
```

### Açıklama

Mobil uygulamanın ana ekranı için gerekli olan:

* Analitik rapor
* Grafik verileri
* Yapay zeka mentor mesajı

bilgilerini tek JSON paketi olarak döndürür.

### Örnek Yanıt

```json
{
  "analiz_raporu": {
    "bugunku_adim": 12500,
    "30_gunluk_ortalama": 11042,
    "haftalik_ortalama": 11800,
    "dao_score": 96,
    "haftalik_tahmin": 82600,
    "en_aktif_gun": "Cumartesi",
    "trend": "📈 Yükselişte"
  },
  "kocluk_mesaji": "Harika bir ilerleme görüyorsun! 12.500 adıma ulaşmış olman heyecan verici...",
  "grafik_verisi": {
    "Pazartesi": 10200,
    "Salı": 9800,
    "Çarşamba": 11500,
    "Perşembe": 11000,
    "Cuma": 13000,
    "Cumartesi": 12500
  }
}
```

---

# 🚀 Yerel Kurulum

## 1. Projeyi Klonlayın

```bash
git clone <repository-url>
cd dao-health-backend
```

## 2. Bağımlılıkları Kurun

```bash
pip install -r requirements.txt
```

## 3. Sunucuyu Başlatın

```bash
uvicorn main_v2:app --host 0.0.0.0 --port 8000
```

## 4. Swagger Arayüzünü Açın

```text
http://localhost:8000/docs
```

---

# 🐳 Docker ile Çalıştırma

Docker image oluşturun:

```bash
docker build -t dao-health-backend .
```

Container başlatın:

```bash
docker run -p 8000:8000 dao-health-backend
```

---

# 📈 DAO Sağlık Skoru Mantığı

DAO Sağlık Skoru, kullanıcının günlük ve haftalık aktivite alışkanlıklarını değerlendiren özel bir metrik olarak tasarlanmıştır.

Skor hesaplanırken:

* Günlük adım sayısı
* Haftalık ortalama
* Aktivite istikrarı
* Trend yönü
* Hedef tamamlama oranı

gibi değişkenler dikkate alınır.

Skor aralığı:

| Skor   | Durum            |
| ------ | ---------------- |
| 0-40   | Düşük Aktivite   |
| 41-70  | Geliştirilebilir |
| 71-90  | İyi              |
| 91-100 | Mükemmel         |

---

# 🗺️ Yol Haritası (Roadmap)

## Mobil Uygulama

* [ ] Flutter ile Android ve iOS uygulaması geliştirilmesi
* [ ] Aktivite halkalarının mobil arayüze entegrasyonu
* [ ] Gerçek zamanlı bildirim sistemi

## Sağlık Entegrasyonları

* [ ] Android Health Connect entegrasyonu
* [ ] Apple HealthKit entegrasyonu
* [ ] Akıllı saat üreticileri için API adaptörleri

## Veri Katmanı

* [ ] SQLite → PostgreSQL geçişi
* [ ] Redis cache katmanı eklenmesi
* [ ] Veri yedekleme ve replikasyon desteği

## Yapay Zeka

* [ ] Uzun dönem sağlık tahmin modelleri
* [ ] Aktivite anomalisi tespiti
* [ ] Kişiselleştirilmiş hedef öneri sistemi
* [ ] Çoklu LLM yönlendirme (Router Architecture)

---

# 🛠️ Kullanılan Teknolojiler

| Teknoloji     | Amaç                  |
| ------------- | --------------------- |
| FastAPI       | REST API Servisi      |
| Pydantic      | Veri Doğrulama        |
| SQLite        | Veri Depolama         |
| NumPy         | Analitik Hesaplamalar |
| Gemini API    | Bulut Yapay Zeka      |
| Gemma 2 2B-IT | Yerel Yapay Zeka      |
| Uvicorn       | ASGI Sunucusu         |
| Docker        | Konteynerleştirme     |

---

# 📄 Lisans

Bu proje eğitim, araştırma ve portföy amaçlı geliştirilmiştir.

---

## 💡 Not

Bu proje; kıdemli yazılım mühendisliği prensipleri, modern backend mimarileri ve yapay zeka destekli geliştirme yaklaşımları kullanılarak tasarlanmış bir sağlık teknolojileri demonstrasyonudur.

## Hazırlayan
**Serdar ÖNAL** | 
**İnşaat Mühendisi & Yapay Zeka Geliştiricisi | 2026**
> "Mühendislik disipliniyle veriyi işliyor, sahadaki arızaları dijital dünyada öngörüyorum."

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/serdarönal1981)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/madsancos)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/sancos)
