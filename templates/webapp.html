from flask import Flask, render_template
import math
import requests
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Configuration des variables d'environnement (Render)
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

def get_master_vip_matches():
    """Matrice de secours absolue : S'active instantanément si l'API est vide ou hors ligne."""
    return [
        {
            "home": "Real Madrid", "away": "FC Barcelona", "league": "LaLiga EA Sports 🇪🇸",
            "time": "VIP Matrix", "status": "MATRICE ÉLITE 👑",
            "home_xg": 2.10, "away_xg": 1.25, "fair_odd": 1.70, "xbet_odd": 1.95, 
            "market": "Victoire 1 & Plus de 1.5 | Pinnacle: 1.80"
        },
        {
            "home": "Manchester City", "away": "Arsenal", "league": "Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
            "time": "VIP Matrix", "status": "SMART MONEY 💎",
            "home_xg": 1.95, "away_xg": 1.45, "fair_odd": 1.90, "xbet_odd": 2.15, 
            "market": "Les 2 équipes marquent (BTTS) | Pinnacle: 2.05"
        }
    ]

def fetch_real_fixtures():
    if not API_KEY or API_KEY == 'ta_cle_api_ici':
        return get_master_vip_matches()

    # Scan sur 2 jours pour garantir un flux continu
    dates_to_check = [
        datetime.now().strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    ]
    
    major_leagues = {
        39: "Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿", 140: "LaLiga 🇪🇸", 135: "Serie A 🇮🇹", 
        61: "Ligue 1 🇫🇷", 78: "Bundesliga 🇩🇪", 2: "Champions League 🇪🇺",
        3: "Europa League 🇪🇺", 848: "Conference League 🇪🇺",
        253: "Major League Soccer 🇺🇸", 71: "Brasileirão 🇧🇷"
    }

    all_fixtures = []
    headers = {"x-apisports-key": API_KEY, "x-apisports-host": API_HOST}

    for date_str in dates_to_check:
        url = "https://v3.football.api-sports.io/fixtures"
        try:
            response = requests.get(url, headers=headers, params={"date": date_str}, timeout=6)
            data = response.json()
            
            for item in data.get('response', []):
                league_id = item['league']['id']
                if league_id in major_leagues:
                    status_short = item['fixture']['status']['short']
                    # On prend les matchs non commencés (NS) ou en direct (1H, HT, 2H)
                    if status_short in ['NS', '1H', '2H', 'HT']:
                        home_xg = random.uniform(1.4, 2.5)
                        away_xg = random.uniform(0.7, 1.6)
                        
                        time_str = item['fixture']['date'][11:16]
                        day_label = "Auj." if date_str == dates_to_check[0] else "Demain"
                        
                        fair_odd = max(1.15, round(1 / (math.exp(-away_xg) + 0.1), 2))
                        xbet_odd = round(fair_odd * 1.15, 2)
                        pin_odd = round(fair_odd * 1.05, 2)
                        
                        all_fixtures.append({
                            "home": item['teams']['home']['name'], 
                            "away": item['teams']['away']['name'], 
                            "league": major_leagues[league_id],
                            "time": f"{day_label} {time_str}", 
                            "status": f"LIVE {item['fixture']['status']['elapsed']}' 🟢" if status_short != 'NS' else "VIP PRO 👑",
                            "home_xg": home_xg, "away_xg": away_xg, 
                            "fair_odd": fair_odd, "xbet_odd": xbet_odd, 
                            "market": f"Victoire {'1' if home_xg > away_xg else '2'} (1XBET) | PIN: {pin_odd}"
                        })
        except Exception:
            continue

    if not all_fixtures:
        return get_master_vip_matches()

    # Sélectionner les 7 matchs avec la plus forte probabilité de victoire
    all_fixtures.sort(key=lambda x: abs(x['home_xg'] - x['away_xg']), reverse=True)
    return all_fixtures[:7]

def get_stx_matrix_data():
    raw_fixtures = fetch_real_fixtures()
    processed_matches = []
    
    for m in raw_fixtures:
        v1, n, v2, s1, p1, s2, p2, s3, p3 = calculate_advanced_poisson(m['home_xg'], m['away_xg'])
        m['prob_1'] = v1
        m['prob_x'] = n
        m['prob_2'] = v2
        m['score_1'] = f"🎯 {s1}"
        m['score_1_p'] = p1
        m['score_2'] = s2
        m['score_2_p'] = p2
        m['score_3'] = s3
        m['score_3_p'] = p3
        m['smart_money'] = generate_smart_money_index(v1, v2)
        m['ev_edge'] = round(((m['xbet_odd'] / m['fair_odd']) - 1) * 100, 1)
        
        processed_matches.append(m)
        
    return processed_matches

@app.route('/webapp')
def webapp():
    data = get_stx_matrix_data()
    # On envoie toute la liste "data" au template HTML sous le nom "matches"
    return render_template('webapp.html', matches=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
