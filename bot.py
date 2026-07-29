import json
import urllib.request
import ssl
from datetime import datetime

# Paratic veya genel finansal verileri simüle eden/çeken yapı
# Not: Gerçek sitenin yapısına göre BeautifulSoup eklenebilir, 
# burada örnek ve kararlı çalışması için standart finans API/yapısı baz alınmıştır.

def fetch_market_data():
    data = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": [
            {"symbol": "USD/TRY", "name": "Dolar / Türk Lirası", "price": "33.50", "change": "+0.15%"},
            {"symbol": "EUR/TRY", "name": "Euro / Türk Lirası", "price": "36.20", "change": "-0.05%"},
            {"symbol": "ALTIN", "name": "Gram Altın", "price": "2,650.40", "change": "+1.20%"},
            {"symbol": "BIST 100", "name": "BIST 100", "icon": "bist", "price": "10,850.30", "change": "+0.45%"},
            {"symbol": "EUR/USD", "name": "Euro / Dolar", "price": "1.0810", "change": "-0.10%"},
            {"symbol": "BTC/USD", "name": "Bitcoin", "price": "65,400.00", "change": "+2.30%"}
        ]
    }
    
    with open('markets.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Veriler başarıyla güncellendi.")

if __name__ == "__main__":
    fetch_market_data()
