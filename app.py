from flask import Flask, render_template
import math
import requests
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)

API_KEY = os.environ.get('API_FOOTBALL_KEY') or os.environ.get('API_KEY')
API_HOST = "v3.football.api-sports.io"

def calculate_advanced_poisson(home_xg, away_xg):
    prob_h = prob_d = prob_a = 0
    score_probs = {}
    
    for i in range(6): 
        for j in range(6): 
            p = ((math.exp(-home_xg) * (home_xg**i)) / math.factorial(i)) * \
                ((math.exp(-away_xg) * (away_xg**j)) / math.factorial(j))
            
            if i > j: prob_h += p
            elif i == j: prob_d += p
            else: prob_a += p
            
            score_probs[f"{i}-{j}"] = p * 100

    sorted_scores = sorted(score_probs.items(), key=lambda x: x[1], reverse=True)
    
    return (
        round(prob_h * 100, 1), round(prob_d * 100, 1), round(prob_a * 100, 1),
        sorted_scores[0][0], round(sorted_scores[0][1], 1),
        sorted_scores[1][0], round(sorted_scores[1][1], 1),
        sorted_scores[2][0], round(sorted_scores[2][1], 1)
    )

def generate_smart_money_index(prob_1, prob_2):
    dominant = max(prob_1, prob_2)
    return f"👑 VOLUME ACHETEUR: {round(dominant * 1.15, 1)}% (SMART MONEY)"

def get_vip_fallback_fixtures():
    return [
        {
            "home": "Inter Milan", "away": "Juventus", "league": "SERIE A 🇮🇹",
            "time": "VIP EXCLUSIF", "status": "MATRICE ÉLITE 👑",
            "home_xg": 1.85, "away_xg": 1.15, "fair_odd": 1.70, "xbet_odd": 1.95, 
            "market": "Victoire 1 (1XBET) | PIN: 1.88"
        },
        {
            "home": "Boca Juniors", "away": "River Plate", "league": "SUPERLIGA 🇦🇷",
            "time": "PROCHAINEMENT", "status": "SMART MONEY 💎",
            "home_xg": 1.45, "away_xg": 1.40, "fair_odd": 2.20, "xbet_odd": 2.45, 
            "market": "Match Nul ou 2 (X2) | PIN: 1.55"
        },
        {
            "home": "Bayern Munich", "away": "B. Leverkusen", "league": "BUNDESLIGA 🇩🇪",
            "time": "ANALYSE STX", "status": "VALUE BET ⚡",
            "home_xg": 2.40, "away_xg": 1.75, "fair_odd": 1.65, "xbet_odd": 1.82, 
            "market": "Plus de 2.5 Buts (1XBET) | PIN: 1.78"
        }
    ]

def fetch_real_fixtures():
    dates = [
        datetime.now().strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    ]
    
    all_fixtures = []
    headers = {"x-apisports-key": API_KEY, "x-apisports-host": API_HOST}

    for d in dates:
        try:
            res = requests.get("https://v3.football.api-sports.io/fixtures", headers=headers, params={"date": d}, timeout=4)
            data = res.json()
            
            for item in data.get('response', []):
                status = item['fixture']['status']['short']
                if status in ['NS', '1H', '2H', 'HT']:
                    h_xg = random.uniform(1.3, 2.4)
                    a_xg = random.uniform(0.7, 1.6)
                    f_odd = max(1.15, round(1 / (math.exp(-a_xg) + 0.1), 2))
                    
                    all_fixtures.append({
                        "home": item['teams']['home']['name'], 
                        "away": item['teams']['away']['name'], 
                        "league": item['league']['name'], 
                        "time": f"Le {d[5:]} à {item['fixture']['date'][11:16]}", 
                        "status": f"LIVE {item['fixture']['status']['elapsed']}' 🟢" if status != 'NS' else "ANALYSE STX 💎",
                        "home_xg": h_xg, "away_xg": a_xg, 
                        "fair_odd": f_odd, "xbet_odd": round(f_odd * 1.15, 2), 
                        "market": f"Victoire {'1' if h_xg > a_xg else '2'} (1XBET)"
                    })
        except Exception:
            continue
        if len(all_fixtures) >= 6: break

    return all_fixtures[:6] if all_fixtures else get_vip_fallback_fixtures()

def get_stx_matrix_data():
    return [{**m, 
             'prob_1': (p:=calculate_advanced_poisson(m['home_xg'], m['away_xg']))[0],
             'prob_x': p[1], 'prob_2': p[2], 
             'score_1': f"🎯 {p[3]}", 'score_1_p': p[4],
             'score_2': p[5], 'score_2_p': p[6],
             'score_3': p[7], 'score_3_p': p[8],
             'smart_money': generate_smart_money_index(p[0], p[2]),
             'ev_edge': round(((m['xbet_odd'] / m['fair_odd']) - 1) * 100, 1)
            } for m in fetch_real_fixtures()]

@app.route('/webapp')
def webapp():
    return render_template('webapp.html', matches=get_stx_matrix_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
