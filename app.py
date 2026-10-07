import os
import time
import json
import requests
import datetime
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "VOTRE_TOKEN_BOTFATHER")
CHAT_ID = os.getenv("CHAT_ID", "-100_VOTRE_ID_CANAL_VIP")
CACHE_FILE = "sent_signals.json"

app = Flask(__name__)

@app.route('/')
def home():
    return "STX Omni-Matrix Bot est actif 24h/24 !", 200

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_to_cache(match_id):
    cache = load_cache()
    if match_id not in cache:
        cache.append(match_id)
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)

def send_telegram_vip(signal):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    message = (
        f"⚡ <b>[STX OMNI-MATRIX - SIGNAL VERROUILLÉ]</b> ⚡\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚽ <b>Match :</b> {signal.get('home', 'Équipe A')} vs {signal.get('away', 'Équipe B')}\n"
        f"🏆 <b>Ligue :</b> {signal.get('league', 'Ligue')}\n"
        f"⏰ <b>Heure :</b> {signal.get('time', 'À venir')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>PRÉDICTIONS MULTI-MARCHÉS :</b>\n"
        f"🔹 <b>Score Exact :</b> <code>{signal.get('exact_score', '2-1')}</code>\n"
        f"🔹 <b>Corners Total :</b> <code>{signal.get('corners_market', '+9.5')}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 <b>CONSENSUS & METRIQUES :</b>\n"
        f"🔥 <b>Synergy Lock (IA) :</b> <code>{signal.get('ai_confidence', 96.5)}%</code>\n"
        f"💧 <b>Chute de cote :</b> {signal.get('odds_drop', 'Détectée')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✍️ <b>Généré par @888stx</b>\n"
        f"📞 <b>Support VIP :</b> +226 74 82 33 24"
    )
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            save_to_cache(signal.get('match_id'))
            print(f"[{datetime.datetime.now()}] ✅ Signal envoyé avec succès.")
    except Exception as e:
        print(f"Erreur d'envoi Telegram : {e}")

def hunt_for_signals():
    print(f"[{datetime.datetime.now()}] 🔎 Scan des opportunités en cours...")
    mock_signal = {
        "match_id": f"MATCH_{int(time.time())}",
        "home": "Real Madrid",
        "away": "Man City",
        "league": "Champions League",
        "time": "20:00",
        "exact_score": "2 - 1",
        "corners_market": "Plus de 9.5 Corners",
        "odds_drop": "Infiltration capital +88%",
        "ai_confidence": 96.5
    }
    cache = load_cache()
    if mock_signal["match_id"] not in cache and mock_signal["ai_confidence"] >= 95.0:
        send_telegram_vip(mock_signal)

scheduler = BackgroundScheduler()
scheduler.add_job(hunt_for_signals, 'interval', minutes=15)
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
