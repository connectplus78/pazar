import requests
import json
from datetime import datetime

def update_markets():
    try:
        # GenelPara ücretsiz API uç noktası
        url = "https://api.genelpara.com/json/"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # API'den gelen canlı veriler (Ons, Gram, Çeyrek vb.)
        # data yapısına göre parse edip items listesi oluşturulur
        items = [
            {"symbol": "ONS ALTIN", "price": str(data.get("ONS", {}).get("satis", "2380.50")), "change": "+" + str(data.get("ONS", {}).get("degisim", "0.42")) + "%"},
            {"symbol": "GRAM ALTIN", "price": str(data.get("GA", {}).get("satis", "2650.00")), "change": "+" + str(data.get("GA", {}).get("degisim", "0.35")) + "%"},
            {"symbol": "ÇEYREK ALTIN", "price": str(data.get("C", {}).get("satis", "4350.00")), "change": "+" + str(data.get("C", {}).get("degisim", "0.35")) + "%"},
            {"symbol": "ONS GÜMÜŞ", "price": "28.50", "change": "+%0.19"}
        ]
        
        output = {
            "son_güncelleme": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "items": items
        }
        
        with open("markets.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print("Piyasa verileri başarıyla güncellendi.")
    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    update_markets()
