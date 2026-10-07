from flask import Flask, render_template
import math

app = Flask(__name__)

# --- MOTEUR MATHÉMATIQUE : LOI DE POISSON V2.4 ---
def calculate_poisson_1x2(home_xg, away_xg):
    prob_h = prob_d = prob_a = 0
    for i in range(6): 
        for j in range(6): 
            p = ((math.exp(-home_xg) * (home_xg**i)) / math.factorial(i)) * \
                ((math.exp(-away_xg) * (away_xg**j)) / math.factorial(j))
            if i > j: prob_h += p
            elif i == j: prob_d += p
            else: prob_a += p
    return round(prob_h*100, 1), round(prob_d*100, 1), round(prob_a*100, 1)

# --- SCANNER DE MARCHÉ & CONSENSUS IA ---
def get_stx_matrix_data():
    live_matches = [
        {
            "home": "Cruzeiro", "away": "Sao Paulo", "league": "Serie A Betano",
            "home_xg": 1.45, "away_xg": 0.85,
            "fair_odd": 1.62, "xbet_odd": 1.85, "market": "Under 2.5 Buts",
            "ai_consensus": "88% Forte Confiance"
        },
        {
            "home": "Arsenal", "away": "Aston Villa", "league": "Premier League",
            "home_xg": 2.10, "away_xg": 0.95,
            "fair_odd": 1.45, "xbet_odd": 1.68, "market": "Victoire 1",
            "ai_consensus": "92% Domination Totale"
        },
        {
            "home": "Juventus", "away": "AS Roma", "league": "Serie A",
            "home_xg": 1.10, "away_xg": 1.05,
            "fair_odd": 3.10, "xbet_odd": 3.50, "market": "Match Nul (X)",
            "ai_consensus": "75% Risque Modéré"
        }
    ]
    
    for m in live_matches:
        v1, n, v2 = calculate_poisson_1x2(m['home_xg'], m['away_xg'])
        m['prob_1'] = v1
        m['prob_x'] = n
        m['prob_2'] = v2
        m['ev_edge'] = round(((m['xbet_odd'] / m['fair_odd']) - 1) * 100, 1)
        
    return live_matches

@app.route('/webapp')
def webapp():
    data = get_stx_matrix_data()
    return render_template('webapp.html', matches=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
