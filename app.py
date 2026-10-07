from flask import Flask, render_template
import math

app = Flask(__name__)

# --- MOTEUR MATHÉMATIQUE POISSON & SCORES EXACTS ---
def calculate_poisson_matrix(home_xg, away_xg):
    prob_h = prob_d = prob_a = 0
    score_probs = {}
    
    for i in range(6): 
        for j in range(6): 
            p = ((math.exp(-home_xg) * (home_xg**i)) / math.factorial(i)) * \
                ((math.exp(-away_xg) * (away_xg**j)) / math.factorial(j))
            
            if i > j: prob_h += p
            elif i == j: prob_d += p
            else: prob_a += p
            
            score_str = f"{i}-{j}"
            score_probs[score_str] = p * 100

    sorted_scores = sorted(score_probs.items(), key=lambda x: x[1], reverse=True)
    
    return (
        round(prob_h * 100, 1), 
        round(prob_d * 100, 1), 
        round(prob_a * 100, 1),
        sorted_scores[0][0], round(sorted_scores[0][1], 1),
        sorted_scores[1][0], round(sorted_scores[1][1], 1),
        sorted_scores[2][0], round(sorted_scores[2][1], 1)
    )

def get_stx_matrix_data():
    raw_fixtures = [
        {
            "home": "Real Madrid", "away": "Villarreal", "league": "La Liga EA Sports",
            "time": "Aujourd'hui, 21:00", "status": "LIVE 74'",
            "home_xg": 2.35, "away_xg": 0.80,
            "fair_odd": 1.38, "xbet_odd": 1.58, "market": "Victoire 1 (Clean)"
        },
        {
            "home": "Inter Milan", "away": "Atalanta", "league": "Serie A Enilive",
            "time": "Aujourd'hui, 20:45", "status": "2ème Mi-Temps",
            "home_xg": 1.85, "away_xg": 1.10,
            "fair_odd": 1.55, "xbet_odd": 1.82, "market": "Plus de 1.5 Buts"
        },
        {
            "home": "Manchester City", "away": "Chelsea", "league": "Premier League",
            "time": "Demain, 17:00", "status": "À venir",
            "home_xg": 2.45, "away_xg": 0.90,
            "fair_odd": 1.42, "xbet_odd": 1.65, "market": "Victoire 1 & Over 1.5"
        }
    ]
    
    processed_matches = []
    for m in raw_fixtures:
        v1, n, v2, s1, p1, s2, p2, s3, p3 = calculate_poisson_matrix(m['home_xg'], m['away_xg'])
        m['prob_1'] = v1
        m['prob_x'] = n
        m['prob_2'] = v2
        m['score_1'] = s1
        m['score_1_p'] = p1
        m['score_2'] = s2
        m['score_2_p'] = p2
        m['score_3'] = s3
        m['score_3_p'] = p3
        m['ev_edge'] = round(((m['xbet_odd'] / m['fair_odd']) - 1) * 100, 1)
        processed_matches.append(m)
        
    return processed_matches

@app.route('/webapp')
def webapp():
    data = get_stx_matrix_data()
    return render_template('webapp.html', matches=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
