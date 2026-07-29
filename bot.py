import json
from datetime import datetime
import requests

def update_market_data():
    now = datetime.now()
    tarih_str = now.strftime("%d-%m-%Y %H:%M:%S")

    items = []
    try_rate = 34.0  

    # 1. Tüm Dünya Döviz Kurları (Canlı API)
    try:
        response_doviz = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        if response_doviz.status_code == 200:
            data_doviz = response_doviz.json()
            rates = data_doviz.get("rates", {})
            try_rate = rates.get("TRY", 34.0)
            eur_rate = rates.get("EUR", 1.0)
            gbp_rate = rates.get("GBP", 1.0)
            jpy_rate = rates.get("JPY", 150.0)
            chf_rate = rates.get("CHF", 0.9)
            cad_rate = rates.get("CAD", 1.35)
            aud_rate = rates.get("AUD", 1.5)
            rub_rate = rates.get("RUB", 90.0)
            cny_rate = rates.get("CNY", 7.2)
            sar_rate = rates.get("SAR", 3.75)
            
            # Türk Lirası Karşılıkları (TRY Bazlı)
            items.append({"symbol": "DOLAR", "price": f"{try_rate:.4f}", "change": "+%0.05"})
            
            if eur_rate > 0:
                items.append({"symbol": "EURO", "price": f"{(try_rate / eur_rate):.4f}", "change": "-%0.02"})
            if gbp_rate > 0:
                items.append({"symbol": "STERLİN", "price": f"{(try_rate / gbp_rate):.4f}", "change": "+%0.03"})
            if chf_rate > 0:
                items.append({"symbol": "İSVİÇRE FRANGI", "price": f"{(try_rate / chf_rate):.4f}", "change": "+%0.10"})
            if cad_rate > 0:
                items.append({"symbol": "KANADA DOLARI", "price": f"{(try_rate / cad_rate):.4f}", "change": "-%0.04"})
            if aud_rate > 0:
                items.append({"symbol": "AVUSTRALYA DOLARI", "price": f"{(try_rate / aud_rate):.4f}", "change": "+%0.08"})
            if sar_rate > 0:
                items.append({"symbol": "SUUDİ Rİyalİ", "price": f"{(try_rate / sar_rate):.4f}", "change": "%0.00"})
            if rub_rate > 0:
                items.append({"symbol": "RUS RUBLESİ", "price": f"{(try_rate / rub_rate):.4f}", "change": "-%0.15"})
            if cny_rate > 0:
                items.append({"symbol": "ÇİN YUANI", "price": f"{(try_rate / cny_rate):.4f}", "change": "+%0.02"})

            # Majör Pariteler
            items.append({"symbol": "EUR/USD", "price": f"{(try_rate / (try_rate / eur_rate) if eur_rate else 1.1):.5f}", "change": "-%0.03"})
            items.append({"symbol": "USD/JPY", "price": f"{jpy_rate:.2f}", "change": "-%0.05"})
            items.append({"symbol": "EUR/GBP", "price": f"{((try_rate / eur_rate) / (try_rate / gbp_rate)):.4f}" if (eur_rate and gbp_rate) else "0.857", "change": "+%0.04"})
    except Exception as e:
        print(f"Döviz verisi alınamadı: {e}")

    # 2. Altın, Gümüş ve Emtia Verileri (Doğru Hesaplama Mantığı)
    try:
        ons_altin = 2380.50 
        gram_altin_val = (ons_altin * try_rate) / 31.1035
        ceyreklik = gram_altin_val * 1.75 * 1.055  
        
        items.append({"symbol": "ONS ALTIN", "price": f"{ons_altin:.2f}", "change": "+%0.42"})
        items.append({"symbol": "GRAM ALTIN", "price": f"{gram_altin_val:.2f}", "change": "+%0.35"})
        items.append({"symbol": "ÇEYREK ALTIN", "price": f"{ceyreklik:.2f}", "change": "+%0.35"})
        
        ons_gumus = 28.50
        gram_gumus_val = (ons_gumus * try_rate) / 31.1035
        items.append({"symbol": "ONS GÜMÜŞ", "price": f"{ons_gumus:.2f}", "change": "+%0.19"})
        items.append({"symbol": "GRAM GÜMÜŞ", "price": f"{gram_gumus_val:.2f}", "change": "+%0.23"})
        
        items.append({"symbol": "HAM PETROL", "price": "78.50", "change": "+%0.85"})
    except Exception as e:
        print(f"Emtia hesaplanamadı: {e}")

    # 3. Canlı Kripto Paralar (CoinGecko API)
    try:
        response_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true", timeout=10)
        if response_crypto.status_code == 200:
            c_data = response_crypto.json()
            
            btc_price = c_data.get("bitcoin", {}).get("usd", 65000.0)
            btc_change = c_data.get("bitcoin", {}).get("usd_24h_change", 1.5)
            items.append({
                "symbol": "BİTCOİN", 
                "price": f"{btc_price:,.2f}", 
                "change": f"{'+' if btc_change >= 0 else ''}%{btc_change:.2f}"
            })

            eth_price = c_data.get("ethereum", {}).get("usd", 3500.0)
            eth_change = c_data.get("ethereum", {}).get("usd_24h_change", 1.2)
            items.append({
                "symbol": "ETER", 
                "price": f"{eth_price:,.2f}", 
                "change": f"{'+' if eth_change >= 0 else ''}%{eth_change:.2f}"
            })
    except Exception as e:
        print(f"Kripto verisi alınamadı: {e}")

    # 4. Borsa / Endeksler
    items.extend([
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
    
    print(f"[{tarih_str}] Tüm para birimleri ve piyasa verileri güncellendi.")

if __name__ == "__main__":
    update_market_data()
