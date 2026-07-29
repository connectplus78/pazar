import json
from datetime import datetime
import requests

def update_market_data():
    url = "https://finans.truncgil.com/v2/today.json"

    print("Canlı piyasa verileri v4 API'den çekiliyor...")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            veri = response.json()
            
            guncelleme = veri.get("Update_Date", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            
            items = []
            haric_tutulanlar = ["Update_Date"] 
            
            for kod, bilgi in veri.items():
                if kod in haric_tutulanlar or not isinstance(bilgi, dict):
                    continue
                
                gorunen_isim = bilgi.get("Name", kod).upper()
                satis = bilgi.get("Selling", "0,00")
                degisim = str(bilgi.get("Change", "%0,00"))
                
                items.append({
                    "symbol": gorunen_isim,
                    "price": str(satis),
                    "change": degisim
                })

            veriler = {
                "last_update": guncelleme,
                "son_güncelleme": guncelleme,
                "items": items
            }
            
            with open("markets.json", "w", encoding="utf-8") as f:
                json.dump(veriler, f, ensure_ascii=False, indent=4)
                
            print(f"Başarılı! v4 API üzerinden {len(items)} birim markets.json dosyasına kaydedildi.")

        else:
            print(f"Hata! Bağlantı kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    update_market_data()
