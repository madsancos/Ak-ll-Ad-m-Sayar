from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import sqlite3
import torch
import os
import requests 
from transformers import AutoTokenizer, AutoModelForCausalLM

from fastapi import FastAPI
# 1. CORS kütüphanesini içeri aktarıyoruz
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 2. Güvenlik duvarından geçebilecek adresleri (Localhost ve Render) tanımlıyoruz
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://smart-pedometer.onrender.com",
]

# 3. FastAPI bekçisine bu kökenlerden gelen tüm isteklere (GET, POST vb.) izin ver diyoruz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında tıkanmamak için geçici olarak her yere açıyoruz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sizin dün geceki mevcut endpoint'iniz aşağıda kalmaya devam edecek:
@app.get("/")
def read_root():
    return {
        "guncelAdim": 11450,
        "hedef": 12000,
        "kalori": 420,
        "mesafe": 7.2,
        "aktifDakika": 55,
        "daoSaglikSkoru": 98,
        "koceMesaji": "Serdar Bey, harika bir gün! Adım hedefinize yaklaşırken Xiaomi tartı verileriniz kas kütlenizin korunduğunu gösteriyor. Yürüyüşe devam!"
    }


app = FastAPI(
    title="DAO Akıllı Sağlık Ajanı API Katmanı - V2",
    description="Mobil uygulama için Hibrit LLM destekli ışık hızında sağlık servisi",
    version="2.0.0"
)

class StepDataInput(BaseModel):
    gun_adi: str
    adim_sayisi: int

class ActivityRepository:
    def __init__(self, db_path="ajan_hafizasi.db"):
        self.db_path = db_path
    def _connect(self):
        return sqlite3.connect(self.db_path)
    def save_step_data(self, gun_adi: str, adim_sayisi: int):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO adim_gecmisi (gun_adi, adim_sayisi) VALUES (?, ?)", (gun_adi, adim_sayisi))
        conn.commit()
        conn.close()
    def get_last_7_days_steps(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT gun_adi, adim_sayisi FROM adim_gecmisi ORDER BY id DESC LIMIT 7")
        rows = cursor.fetchall()
        conn.close()
        return {gun: adim for gun, adim in reversed(rows)} if rows else {}
    def get_last_30_days_average(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(adim_sayisi) FROM adim_gecmisi LIMIT 30")
        avg = cursor.fetchone()[0]
        conn.close()
        return int(avg) if avg else 6500

class ActivityAnalyzer:
    def __init__(self, steps_dict, last_30_days_avg=6500):
        self.steps_dict = steps_dict
        self.steps_data = list(steps_dict.values())
        self.last_30_days_avg = last_30_days_avg
    def calculate_dao_score(self):
        if not self.steps_data: return 0
        today_steps = self.steps_data[-1]
        return int(min((today_steps / 10000) * 40, 40) + max(30 - (np.std(self.steps_data)/1000 if len(self.steps_data)>1 else 0), 10) + 30)
    def generate_report(self):
        if not self.steps_data: return {}
        return {
            "bugunku_adim": self.steps_data[-1],
            "30_gunluk_ortalama": self.last_30_days_avg,
            "haftalik_ortalama": int(np.mean(self.steps_data)),
            "dao_score": self.calculate_dao_score(),
            "haftalik_tahmin": int(np.mean(self.steps_data) * 7),
            "en_aktif_gun": list(self.steps_dict.keys())[np.argmax(self.steps_data)],
            "trend": "📈 Yükselişte" if self.steps_data[-1] > self.last_30_days_avg else "📉 Dinlenmede"
        }

class HibritSaglikKocu:
    def __init__(self):
        self.api_key = os.getenv("Enter_API_key")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        self.model_dir = "/kaggle/input/models/google/gemma-2/transformers/gemma-2-2b-it/2"
        self.tokenizer = None
        self.local_model = None

    def _init_local_model(self):
        if self.local_model is None:
            print("⚠️ Bulut API yanıt vermedi, yerel Gemma 2 RAM'e yükleniyor...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            self.local_model = AutoModelForCausalLM.from_pretrained(
                self.model_dir, torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32, device_map="auto"
            )

    def günlük_analiz_ve_mentorluk(self, analiz_raporu):
        sistem_mesaji = "Sen samimi ve profesyonel bir Kişisel Sağlık Koçusun. Verileri Türkçe yorumla, motivasyon ver ve mesajı düzgünce bitir."
        rapor_metni = f"Bugün Atılan Adım: {analiz_raporu['bugunku_adim']}, Ortalama: {analiz_raporu['haftalik_ortalama']}, Trend: {analiz_raporu['trend']}, DAO Skoru: {analiz_raporu['dao_score']}/100."
        prompt = f"{sistem_mesaji}\n\n{rapor_metni}"

        try:
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(self.gemini_url, json=payload, headers={"Content-Type": "application/json"}, timeout=5)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            print(f"Bulut hatası: {e}. Yerel modele geçiliyor...")

        self._init_local_model()
        local_prompt = f"<bos><start_of_turn>user\n{sistem_mesaji}\n\n{rapor_metni}<end_of_turn>\n<start_of_turn>model\n"
        inputs = self.tokenizer(local_prompt, return_tensors="pt").to(self.local_model.device)
        input_length = inputs["input_ids"].shape[-1]
        with torch.no_grad():
            outputs = self.local_model.generate(**inputs, max_new_tokens=400, temperature=0.7, do_sample=True, repetition_penalty=1.2)
        return self.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)

repo = ActivityRepository()
coach = HibritSaglikKocu()

@app.get("/")
def read_root():
    return {"status": "online", "message": "DAO Akıllı Sağlık Ajanı API Katmanı V2 Aktif!"}

@app.post("/api/steps")
def add_step_data(data: StepDataInput):
    try:
        repo.save_step_data(data.gun_adi, data.adim_sayisi)
        return {"success": True, "message": f"{data.gun_adi} günü için {data.adim_sayisi} adım kaydedildi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard")
def get_dashboard_data():
    haftalik_veri = repo.get_last_7_days_steps()
    if not haftalik_veri:
        raise HTTPException(status_code=404, detail="Veritabanında analiz edilecek veri bulunamadı.")
    rapor = ActivityAnalyzer(steps_dict=haftalik_veri, last_30_days_avg=repo.get_last_30_days_average()).generate_report()
    return {"analiz_raporu": rapor, "kocluk_mesaji": coach.günlük_analiz_ve_mentorluk(rapor), "grafik_verisi": haftalik_veri}
