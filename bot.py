import json
from datetime import datetime
import requests

def update_market_data():
    now = datetime.now()
    tarih_str = now.strftime("%d-%m-%Y %H:%M:%S")

    items = []

    # 1. Canlı Döviz ve Altın Verileri (GenelPara API)
    try:
        response = requests.get("https://api.genelpara.com/json/", timeout=10)
        print("API Yanıt Kodu:", response.status_code)
        
        if response.status_code == 200:
            data = response.json()
            print("API Verisi Alındı.")
            
            # Majör Dövizler
            if "USD" in data:
                items.append({"symbol": "DOLAR", "price": str(data["USD"].get("satis", "0")), "change": f"%{data['USD'].get('degisim', '0')}"})
            if "EUR" in data:
                items.append({"symbol": "EURO", "price": str(data["EUR"].get("satis", "0")), "change": f"%{data['EUR'].get('degisim', '0')}"})
            if "GBP" in data:
                items.append({"symbol": "STERLİN", "price": str(data["GBP"].get("satis", "0")), "change": f"%{data['GBP'].get('degisim', '0')}"})
            if "CHF" in data:
                items.append({"symbol": "İSVİÇRE FRANGI", "price": str(data["CHF"].get("satis", "0")), "change": f"%{data['CHF'].get('degisim', '0')}"})
            if "CAD" in data:
                items.append({"symbol": "KANADA DOLARI", "price": str(data["CAD"].get("satis", "0")), "change": f"%{data['CAD'].get('degisim', '0')}"})
            if "AUD" in data:
                items.append({"symbol": "AVUSTRALYA DOLARI", "price": str(data["AUD"].get("satis", "0")), "change": f"%{data['AUD'].get('degisim', '0')}"})
            if "SAR" in data:
                items.append({"symbol": "SUUDİ RİYALİ", "price": str(data["SAR"].get("satis", "0")), "change": f"%{data['SAR'].get('degisim', '0')}"})
            if "RUB" in data:
                items.append({"symbol": "RUS RUBLESİ", "price": str(data["RUB"].get("satis", "0")), "change": f"%{data['RUB'].get('degisim', '0')}"})
            if "CNY" in data:
                items.append({"symbol": "ÇİN YUANI", "price": str(data["CNY"].get("satis", "0")), "change": f"%{data['CNY'].get('degisim', '0')}"})
            if "JPY" in data:
                items.append({"symbol": "JAPON YENİ", "price": str(data["JPY"].get("satis", "0")), "change": f"%{data['JPY'].get('degisim', '0')}"})

            # Pariteler
            if "EURUSD" in data:
                items.append({"symbol": "EUR/USD", "price": str(data["EURUSD"].get("satis", "0")), "change": f"%{data['EURUSD'].get('degisim', '0')}"})
            if "USDJPY" in data:
                items.append({"symbol": "USD/JPY", "price": str(data["USDJPY"].get("satis", "0")), "change": f"%{data['USDJPY'].get('degisim', '0')}"})
            if "EURGBP" in data:
                items.append({"symbol": "EUR/GBP", "price": str(data["EURGBP"].get("satis", "0")), "change": f"%{data['EURGBP'].get('degisim', '0')}"})

            # Altın Türleri
            if "ONS" in data:
                items.append({"symbol": "ONS ALTIN", "price": str(data["ONS"].get("satis", "0")), "change": f"%{data['ONS'].get('degisim', '0')}"})
            if "GA" in data:
                items.append({"symbol": "GRAM ALTIN", "price": str(data["GA"].get("satis", "0")), "change": f"%{data['GA'].get('degisim', '0')}"})
            if "C" in data:
                items.append({"symbol": "ÇEYREK ALTIN", "price": str(data["C"].get("satis", "0")), "change": f"%{data['C'].get('degisim', '0')}"})
            if "YARIM" in data:
                items.append({"symbol": "YARIM ALTIN", "price": str(data["YARIM"].get("satis", "0")), "change": f"%{data['YARIM'].get('degisim', '0')}"})
            if "ATA" in data:
                items.append({"symbol": "ATA ALTIN", "price": str(data["ATA"].get("satis", "0")), "change": f"%{data['ATA'].get('degisim', '0')}"})
            if "GUMUS" in data:
                items.append({"symbol": "GRAM GÜMÜŞ", "price": str(data["GUMUS"].get("satis", "0")), "change": f"%{data['GUMUS'].get('degisim', '0')}"})
        else:
            print("GenelPara API HTTP Hatası döndürdü.")
    except Exception as e:
        print(f"GenelPara API kritik hata: {e}")

    # 2. Canlı Kripto Paralar (CoinGecko API)
    try:
        response_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true", timeout=10)
        if response_crypto.status_code == 200:
            c_data = response_crypto.json()
            
            if "bitcoin" in c_data:
                btc = c_data["bitcoin"]
                items.append({"symbol": "BİTCOİN", "price": f"{btc.get('usd', 0):,.2f}", "change": f"{'+' if btc.get('usd_24h_change', 0) >= 0 else ''}%{btc.get('usd_24h_change', 0):.2f}"})
            if "ethereum" in c_data:
                eth = c_data["ethereum"]
                items.append({"symbol": "ETER", "price": f"{eth.get('usd', 0):,.2f}", "change": f"{'+' if eth.get('usd_24h_change', 0) >= 0 else ''}%{eth.get('usd_24h_change', 0):.2f}"})
    except Exception as e:
        print(f"Kripto hatası: {e}")

    # 3. Borsa ve Emtialar
    items.extend([
        {"symbol": "ONS GÜMÜŞ", "price": "31.50", "change": "+%0.19"},
        {"symbol": "HAM PETROL", "price": "78.50", "change": "+%0.85"},
        {"symbol": "THYAO", "price": "298.50", "change": "-%1.57"},
        {"symbol": "ASELS", "price": "62.75", "change": "-%0.35"},
        {"symbol": "PETKM", "price": "21.95", "change": "-%1.53"},
        {"symbol": "BİST 100", "price": "10450.20", "change": "+%1.12"}
    ])

    veriler = {
        "son_güncelleme": tarih_str,
        "items": items
    }

    with open("markets.json", "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)
    
    print(f"[{tarih_str}] JSON dosyası güncellendi. Toplam öğe sayısı: {len(items)}")

if __name__ == "__main__":
    update_market_data()
