import json
from datetime import datetime
import requests

def update_market_data():
    # v4 API adresi olarak güncellendi
    url = "https://finans.truncgil.com/v4/today.json"

    print("Canlı piyasa verileri v4 API'den çekiliyor...")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            veri = response.json()
            
            guncelleme = veri.get("Update_Date", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            
            items = []
            html_orta = ""
            kart_sayisi = 0
            
            haric_tutulanlar = ["Update_Date"] 
            
            ikonlar = {
                "USD": "💵", "EUR": "💶", "GBP": "💷", "CHF": "🇨🇭", "CAD": "🇨🇦", 
                "AUD": "🇦🇺", "RUB": "🇷🇺", "CNY": "🇨🇳", "SAR": "🇸🇦", "JPY": "🇯🇵",
                "AZN": "🇦🇿", "BGN": "🇧🇬", "DKK": "🇩🇰", "NOK": "🇳🇴", "SEK": "🇸🇪",
                "KWD": "🇰🇼", "IRR": "🇮🇷", "IQD": "🇮🇶", "SYP": "🇸🇾", "PKR": "🇵🇰",
                "gram-altin": "🪙", "ceyrek-altin": "🎖️", "yarim-altin": "🏅", 
                "tam-altin": "🏆", "ata-altin": "🥇", "resat-altin": "👑", 
                "bilezik": "💍", "gumus": "⛓️", "ons": "🌐", "BIST_100": "📈"
            }

            for kod, bilgi in veri.items():
                if kod in haric_tutulanlar or not isinstance(bilgi, dict):
                    continue
                
                gorunen_isim = bilgi.get("Name", kod).upper()
                alis = bilgi.get("Buying", "0,00")
                satis = bilgi.get("Selling", "0,00")
                degisim = str(bilgi.get("Change", "%0,00"))
                
                ikon = ikonlar.get(kod, "💱")
                
                items.append({
                    "symbol": gorunen_isim,
                    "price": str(satis),
                    "change": degisim
                })
                
                if degisim.startswith("%-"):
                    renk_class = "dususte"
                    yon_ikon = "▼"
                elif degisim == "%0,00" or degisim == "%0":
                    renk_class = "notr"
                    yon_ikon = "-"
                else:
                    renk_class = "artise"
                    yon_ikon = "▲"
                    
                temiz_degisim = degisim.replace("%", "")
                
                html_orta += f"""
                <div class="kart">
                    <div class="ust-kisim">
                        <div class="isim">{ikon} {gorunen_isim}</div>
                        <div class="degisim {renk_class}">{yon_ikon} %{temiz_degisim}</div>
                    </div>
                    <div class="fiyat-satir">
                        <span class="etiket">Alış:</span>
                        <span class="deger">{alis} ₺</span>
                    </div>
                    <div class="fiyat-satir">
                        <span class="etiket">Satış:</span>
                        <span class="deger">{satis} ₺</span>
                    </div>
                </div>
                """
                kart_sayisi += 1

            # DÜZELTME BURADA YAPILDI: "son_güncelleme" yerine "last_update" yazıldı
            veriler = {
                "last_update": guncelleme,
                "items": items
            }
            with open("markets.json", "w", encoding="utf-8") as f:
                json.dump(veriler, f, ensure_ascii=False, indent=4)

            html_ust = f"""
            <!DOCTYPE html>
            <html lang="tr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Canlı Piyasa - İnadına TV</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
                <style>
                    body {{ font-family: 'Poppins', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 15px; }}
                    .header {{ text-align: center; margin-bottom: 20px; padding-top: 10px; }}
                    .baslik {{ font-size: 24px; font-weight: 800; color: #fbbf24; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
                    .alt-baslik {{ font-size: 13px; color: #94a3b8; font-weight: 500; }}
                    .grid-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }}
                    .kart {{ background: #1e293b; border-radius: 12px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); border-top: 3px solid #fbbf24; }}
                    .ust-kisim {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #334155; padding-bottom: 8px; gap: 8px; }}
                    .isim {{ font-size: 14px; font-weight: 600; color: #f1f5f9; display: flex; align-items: center; gap: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
                    .fiyat-satir {{ display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 14px; }}
                    .etiket {{ color: #94a3b8; font-size: 12px; }}
                    .deger {{ font-weight: 600; color: #38bdf8; }}
                    .degisim {{ font-size: 11px; font-weight: 600; padding: 3px 6px; border-radius: 6px; white-space: nowrap; flex-shrink: 0; }}
                    .artise {{ background: rgba(34, 197, 94, 0.2); color: #4ade80; }}
                    .dususte {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
                    .notr {{ background: rgba(148, 163, 184, 0.2); color: #94a3b8; }}
                    .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #64748b; line-height: 1.6; }}
                    .marka {{ color: #fbbf24; font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <div class="baslik">📉 CANLI PİYASA</div>
                    <div class="alt-baslik">Tüm Döviz, Altın ve Borsa Kurları (v4)</div>
                </div>
                <div class="grid-container">
            """

            html_alt = f"""
                </div>
                <div class="footer">
                    © 2026 <span class="marka">İnadına TV</span> Özel Servisi<br>
                    Son Güncelleme: {guncelleme}
                </div>
            </body>
            </html>
            """

            if kart_sayisi > 0:
                with open("index.html", "w", encoding="utf-8") as dosya:
                    dosya.write(html_ust + html_orta + html_alt)
                print(f"Başarılı! v4 API üzerinden {kart_sayisi} birim kaydedildi.")
            else:
                print("Veri alındı ancak işlenecek kur bulunamadı.")

        else:
            print(f"Hata! Bağlantı kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    update_market_data()
