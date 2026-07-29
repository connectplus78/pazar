import json
import time
from datetime import datetime
import requests  # Eğer canlı veri çekiyorsanız (requests kütüphanesi gerekir)

def update_market_data():
    # Türkiye saatine göre güncel tarih ve saat (Örn: 29-07-2026 17:35)
    now = datetime.now()
    tarih_str = now.strftime("%d-%m-%Y %H:%M")

    # Buraya piyasa verilerinizi ekleyebilirsiniz (API'den çekebilir veya manuel güncelleyebilirsiniz)
    veriler = {
        "last_update": tarih_str,
        "items": [
            {"symbol": "USD/TRY", "price": "32.50", "change": "%+0.50"},
            {"symbol": "EUR/TRY", "price": "35.20", "change": "%-0.10"},
            {"symbol": "ALTIN", "price": "2450.00", "change": "%+1.20"},
            {"symbol": "BIST 100", "price": "10500.00", "change": "%+0.85"}
        ]
    }

    # Verileri markets.json dosyasına kaydet
    with open("markets.json", "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)
    
    print(f"[{tarih_str}] markets.json başarıyla güncellendi.")

# Botun çalışmasını istediğiniz döngü (Örn: Her 2 saniyede bir veya dakikada bir)
if __name__ == "__main__":
    while True:
        update_market_data()
        time.sleep(2)  # 2 saniyede bir güncelleme yapar (istediğiniz süreye göre ayarlayabilirsiniz)
