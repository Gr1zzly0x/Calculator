from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # Get form values
    balance = float(request.form['balance'])
    house_edge = float(request.form['house_edge'])
    wager_requirement_multiplier_min = float(request.form['wager_requirement_multiplier_min'])
    wager_requirement_multiplier_max = float(request.form['wager_requirement_multiplier_max'])

    # Calculate wager amounts
    bet = balance / 10
    total_wager_needed_min = balance * wager_requirement_multiplier_min
    total_wager_needed_max = balance * wager_requirement_multiplier_max
    simulations = 1000

    # Define bet_win_lose function
    def bet_win_lose():
        random_number = random.random()
        if random_number > 0.5:
            return True
        else:
            return False

    # Calculate final balance for minimum wager requirement
    def final_balance_lower():
        total_bet = 0
        bal = balance
        global bet
        global house_edge
        global wager_requirement_multiplier_min
        global total_wager_needed_min

        while total_bet < total_wager_needed_min and bal > 0:
            if bal >= bet:
                if bet_win_lose():
                    bal += bet * (1-(2*house_edge))
                    total_bet += bet
                else:
                    bal -= bet
                    total_bet += bet
            else:
                if bet_win_lose():
                    bal += bal * (1-(2*house_edge))
                    total_bet += bal
                else:
                    bal -= bal
                    total_bet += bal

        return bal

    # Calculate final balance for maximum wager requirement
    def final_balance_upper():
        total_bet = 0
        bal = balance
        global bet
        global house_edge
        global wager_requirement_multiplier_max
        global total_wager_needed_max

        while total_bet < total_wager_needed_max and bal > 0:
            if bal >= bet:
                if bet_win_lose():
                    bal += bet * (1-(2*house_edge))
                    total_bet += bet
                else:
                    bal -= bet
                    total_bet += bet
            else:
                if bet_win_lose():
                    bal += bal * (1-(2*house_edge))
                    total_bet += bal
                else:
                    bal -= bal
                    total_bet += bal

        return bal

sum = 0
for i in range(simulations):
    sum += final_balance_lower()

print(f"The final balance after a {wager_requirement_multiplier_min}x wager requirement of ${total_wager_needed_min} : {sum/simulations}")

sum = 0
for i in range(simulations):
    sum += final_balance_upper()

print(f"The final balance after a {wager_requirement_multiplier_max}x wager requirement of ${total_wager_needed_max} since the streamer played over the minimum : {sum/simulations}")
       
