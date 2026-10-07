from flask import Flask, render_template
import math

app = Flask(__name__)

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
            "home": "Paris Saint-Germain", "away": "Marseille", "league": "Ligue 1 McDonald's",
            "time": "Ce Soir, 20:45", "status": "ANALYSE LIVE",
            "home_xg": 2.25, "away_xg": 0.85,
            "fair_odd": 1.45, "xbet_odd": 1.72, "market": "Victoire 1 & Plus de 1.5"
        },
        {
            "home": "FC Barcelona", "away": "Atletico Madrid", "league": "La Liga EA Sports",
            "time": "Ce Soir, 21:00", "status": "MATRICE VIP",
            "home_xg": 1.95, "away_xg": 1.05,
            "fair_odd": 1.62, "xbet_odd": 1.90, "market": "Les deux équipes marquent"
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
