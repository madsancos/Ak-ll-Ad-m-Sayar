# 1. Adım: İnternetten resmi ve temiz bir Python işletim sistemi çek
FROM python:3.10-slim

# 2. Adım: Sunucunun içinde /app adında bir çalışma klasörü (şantiye odası) aç
WORKDIR /app

# 3. Adım: Gerekli sistem araçlarını yükle (SQLite ve GCC derleyicileri için)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Adım: Bizim malzeme listemizi sunucunun içine kopyala
COPY requirements.txt .

# 5. Adım: Tüm kütüphaneleri sunucuya otomatik monte et
RUN pip install --no-cache-dir -r requirements.txt

# 6. Adım: Kodlarımızın hepsini sunucunun içine aktar
COPY . .

# 7. Adım: Dış dünyadan erişim için 8000 numaralı kapıyı (portu) aç
EXPOSE 8000

# 8. Adım: Şalteri kaldır ve API'yi 7/24 canlı olarak başlat!
CMD ["uvicorn", "main_v2:app", "--host", "0.0.0.0", "--port", "8000"]
