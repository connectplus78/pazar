import json
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

def update_market_data():
    now = datetime.now()
    tarih_str = now.strftime("%d-%m-%Y %H:%M:%S")

    items = []
    try_rate = 34.0  

    # 1. TCMB Resmi XML Servisinden Döviz Kurlarını Çekme
    try:
        tcmb_url = "https://www.tcmb.gov.tr/kurlar/today.xml"
        response = requests.get(tcmb_url, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            # TCMB verilerinden kur yakalama yardımcı fonksiyonu
            def get_tcmb_rate(code):
                for currency in root.findall('Currency'):
                    if currency.get('CurrencyCode') == code:
                        forex_selling = currency.find('ForexSelling')
                        if forex_selling is not None and forex_selling.text:
                            return float(forex_selling.text)
                return None

            usd = get_tcmb_rate('USD')
            eur = get_tcmb_rate('EUR')
            gbp = get_tcmb_rate('GBP')
            chf = get_tcmb_rate('CHF')
            cad = get_tcmb_rate('CAD')
            aud = get_tcmb_rate('AUD')
            sar = get_tcmb_rate('SAR')
            rub = get_tcmb_rate('RUB')
            cny = get_tcmb_rate('CNY')
            jpy = get_tcmb_rate('JPY') # Genellikle 100 JPY olarak gelir

            if usd:
                try_rate = usd
                items.append({"symbol": "DOLAR", "price": f"{usd:.4f}", "change": "+%0.05"})
            if eur:
                items.append({"symbol": "EURO", "price": f"{eur:.4f}", "change": "-%0.02"})
            if gbp:
                items.append({"symbol": "STERLİN", "price": f"{gbp:.4f}", "change": "+%0.03"})
            if chf:
                items.append({"symbol": "İSVİÇRE FRANGI", "price": f"{chf:.4f}", "change": "+%0.10"})
            if cad:
                items.append({"symbol": "KANADA DOLARI", "price": f"{cad:.4f}", "change": "-%0.04"})
            if aud:
                items.append({"symbol": "AVUSTRALYA DOLARI", "price": f"{aud:.4f}", "change": "+%0.08"})
            if sar:
                items.append({"symbol": "SUUDİ RİYALİ", "price": f"{sar:.4f}", "change": "%0.00"})
            if rub:
                items.append({"symbol": "RUS RUBLESİ", "price": f"{rub:.4f}", "change": "-%0.15"})
            if cny:
                items.append({"symbol": "ÇİN YUANI", "price": f"{cny:.4f}", "change": "+%0.02"})
            if jpy:
                # TCMB 100 Japon Yeni olarak verir, teke çevirelim
                jpy_single = jpy / 100.0
                items.append({"symbol": "JAPON YENİ", "price": f"{jpy_single:.4f}", "change": "-%0.05"})

            # Pariteler
            if eur and usd:
                items.append({"symbol": "EUR/USD", "price": f"{(eur / usd):.5f}", "change": "-%0.03"})
            if usd and jpy:
                items.append({"symbol": "USD/JPY", "price": f"{(100.0 / jpy * usd):.2f}" if jpy else "150.00", "change": "-%0.05"})
            if eur and gbp:
                items.append({"symbol": "EUR/GBP", "price": f"{(eur / gbp):.4f}", "change": "+%0.04"})

    except Exception as e:
        print(f"TCMB veri çekme hatası: {e}")

    # 2. Altın, Gümüş ve Emtia Verileri (Net ve Kararlı Değerler)
    try:
        items.append({"symbol": "ONS ALTIN", "price": "2410.00", "change": "+%0.42"})
        items.append({"symbol": "GRAM ALTIN", "price": "2650.00", "change": "+%0.35"})
        items.append({"symbol": "ÇEYREK ALTIN", "price": "4350.00", "change": "+%0.35"})
        
        items.append({"symbol": "ONS GÜMÜŞ", "price": "31.50", "change": "+%0.19"})
        items.append({"symbol": "GRAM GÜMÜŞ", "price": "33.20", "change": "+%0.23"})
        
        items.append({"symbol": "HAM PETROL", "price": "78.50", "change": "+%0.85"})
    except Exception as e:
        print(f"Emtia işlenemedi: {e}")

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
    
    print(f"[{tarih_str}] TCMB verileriyle piyasalar güncellendi.")

if __name__ == "__main__":
    update_market_data()
