import os
import json
import win32com.client
import pythoncom
import time
import pandas as pd
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# 📌 Flask Uygulaması Başlatılıyor
app = Flask(__name__)
CORS(app)

# 📌 Excel Dosyasının Tam Yolu
EXCEL_FILE = r"C:\Users\Raporlama-2\Desktop\cirolu_ik_calisma.xlsm"
JSON_FILE_PATH = "kpi_data.json"

# 🔥 **Excel Arka Planda Açık Kalmasını Engellemek İçin Kill Fonksiyonu**
def kill_excel_process():
    os.system("taskkill /F /IM excel.exe")

# ✅ **VBA Makrosunu Çalıştıran Fonksiyon**
def run_vba_macro(macro_name, *args):
    try:
        pythoncom.CoInitialize()  # 📌 Windows COM bileşenlerini başlat
        print("📌 Excel Açılıyor...")

        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False  # 📌 Arka planda çalıştır
        excel.DisplayAlerts = False  # 📌 Uyarıları kapat
        excel.AskToUpdateLinks = False  # 📌 Güncelleme uyarıları kapat

        try:
            wb = excel.Workbooks(EXCEL_FILE)
        except:
            wb = excel.Workbooks.Open(EXCEL_FILE, ReadOnly=False)

        print(f"📌 Açılan Dosya: {EXCEL_FILE}")

        # 🔥 **Makroyu Çalıştır**
        if args:
            macro_call = f"'{wb.Name}'!{macro_name}('{args[0]}', '{args[1]}', '{args[2]}')"
            print(f"📌 Çalıştırılan Makro: {macro_call}")
            excel.Application.Run(macro_call)
        else:
            print(f"📌 Çalıştırılan Makro: {macro_name}")
            excel.Application.Run(macro_name)

        wb.Save()
        wb.Close(SaveChanges=True)
        excel.Quit()

        # 🔥 **Excel Bellekten Temizlensin**
        del wb
        del excel
        pythoncom.CoUninitialize()
        time.sleep(1)

        print("✅ VBA Makrosu Başarıyla Çalıştırıldı!")
        return {"success": f"{macro_name} çalıştırıldı."}
    except Exception as e:
        print(f"❌ VBA Çalıştırma Hatası: {e}")
        return {"error": str(e)}

# ✅ **Excel'deki Güncel KPI Verilerini JSON Formatına Çevirme**
def safe_get(df, row, col, default=0):
    try:
        value = df.iloc[row, col]
        if pd.isna(value):
            return default
        if isinstance(value, str):
            return value.strip().encode("utf-8", "ignore").decode("utf-8")
        return value
    except IndexError:
        return default

def read_kpi_data():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name="Sayfa2", header=None, encoding_errors='replace')

        departmanlar = list(df.iloc[:, 7].dropna().astype(str).unique())
        magazalar = list(df.iloc[:, 21].dropna().astype(str).unique())

        kpi_data = {
            "magazalar": magazalar,
            "departmanlar": departmanlar,
            "cinsiyetler": ["ERKEK", "BAYAN"],
            "toplamCalisan": int(safe_get(df, 1, 2)),
            "bayanSayisi": int(safe_get(df, 3, 2)),
            "erkekSayisi": int(safe_get(df, 4, 2)),
            "girenPersonel": int(safe_get(df, 5, 2)),
            "cikanPersonel": int(safe_get(df, 6, 2)),
            "ayrilmaOrani": round(float(safe_get(df, 6, 3, 0)), 4),
            "ortalamaYas": float(safe_get(df, 14, 2)),  
            "personelBasiCiro": float(safe_get(df, 36, 2)),  
            "egitimMaster": int(safe_get(df, 8, 2)),  
            "egitimUniversite": int(safe_get(df, 9, 2)),
            "egitimYuksekOkul": int(safe_get(df, 10, 2)),
            "egitimLise": int(safe_get(df, 11, 2)),
            "egitimIlkogretim": int(safe_get(df, 12, 2)),
            "egitimIlkOkul": int(safe_get(df, 13, 2)),
            "deneyim5YilUzeri": int(safe_get(df, 16, 2)),
            "deneyim4Yil": int(safe_get(df, 17, 2)),
            "deneyim3Yil": int(safe_get(df, 18, 2)),
            "deneyim2Yil": int(safe_get(df, 19, 2)),
            "deneyim1Yil": int(safe_get(df, 20, 2)),
            "deneyim6_12Ay": int(safe_get(df, 21, 2)),
            "sigaraEvet": int(safe_get(df, 24, 2)),  
            "sigaraHayir": int(safe_get(df, 23, 2)),  
            "ehliyetA": int(safe_get(df, 26, 2)),
            "ehliyetB": int(safe_get(df, 27, 2)),
            "ehliyetC": int(safe_get(df, 28, 2)),
            "ehliyetD": int(safe_get(df, 29, 2)),
            "ehliyetE": int(safe_get(df, 30, 2)),
            "ehliyetY": int(safe_get(df, 31, 2)),
            "medeniHalE": int(safe_get(df, 33, 2)),
            "medeniHalB": int(safe_get(df, 34, 2)),
            "medeniHalD": int(safe_get(df, 35, 2)),
        }

        with open(JSON_FILE_PATH, "w", encoding="utf-8-sig") as file:
            json.dump(kpi_data, file, ensure_ascii=False, indent=4)

        return kpi_data
    except Exception as e:
        return {"error": f"Excel okuma hatası: {str(e)}"}

# ✅ **JSON Verilerini Döndüren API**
@app.route('/kpi_data.json', methods=['GET'])
def get_kpi_data():
    try:
        with open(JSON_FILE_PATH, "rb") as file:
            raw_data = file.read()
            data = json.loads(raw_data.decode("utf-8", "ignore"))

        response = make_response(jsonify(data))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response
    except Exception as e:
        return jsonify({"error": f"JSON okuma hatası: {str(e)}"})

# ✅ **Kullanıcı Filtre Seçtiğinde Çalışacak API**
@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    try:
        data = request.json
        print(f"📌 Filtreleme Verisi: {data}")

        # Eğer "Tümü" seçilmişse Excel'deki hücreleri temizle
        magaza = "" if data.get("magaza", "") == "Tümü" else data.get("magaza", "")
        departman = "" if data.get("departman", "") == "Tümü" else data.get("departman", "")
        cinsiyet = "" if data.get("cinsiyet", "") == "Tümü" else data.get("cinsiyet", "")

        print(f"📌 Güncellenmiş Parametreler -> Magaza: {magaza}, Departman: {departman}, Cinsiyet: {cinsiyet}")

        pythoncom.CoInitialize()
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        wb = excel.Workbooks.Open(EXCEL_FILE, ReadOnly=False)
        ws = wb.Sheets("Sayfa2")

        ws.Range("Z1").Value = magaza
        ws.Range("Z2").Value = departman
        ws.Range("Z3").Value = cinsiyet
        wb.Save()
        wb.Close()
        excel.Quit()
        pythoncom.CoUninitialize()

        # 🔥 **Makroyu Çalıştır**
        result = run_vba_macro("FiltreUygula", magaza, departman, cinsiyet)

        # 🔥 **Excel'i zorla kapat ki salt okunur hatası olmasın**
        kill_excel_process()

        return jsonify(result)
    except Exception as e:
        print(f"❌ Hata: {e}")
        return jsonify({"error": str(e)})
    
    # ✅ **Kullanıcı Filtre Seçtiğinde Çalışacak API**
@app.route('/clear_filters', methods=['POST'])
def clear_filters():
    try:
        print("📌 Filtreler temizleniyor...")

        pythoncom.CoInitialize()
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        wb = excel.Workbooks.Open(EXCEL_FILE, ReadOnly=False)
        ws = wb.Sheets("Sayfa2")

        # Filtreleri temizle
        ws.Range("Z1").Value = ""
        ws.Range("Z2").Value = ""
        ws.Range("Z3").Value = ""

        wb.Save()
        wb.Close()
        excel.Quit()
        pythoncom.CoUninitialize()

        # VBA Makrosunu çalıştırarak filtreleri temizle
        result = run_vba_macro("FiltreleriTemizle")

        # Excel sürecini kapat
        kill_excel_process()

        return jsonify(result)
    except Exception as e:
        print(f"❌ Filtreleri temizleme hatası: {e}")
        return jsonify({"error": str(e)})

    
# ✅ **Flask Sunucusunu Başlat**
if __name__ == '__main__':
    os.environ["PYTHONIOENCODING"] = "utf-8"
    app.run(host="0.0.0.0", port=8000, debug=True)
