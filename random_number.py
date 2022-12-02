from flask import Flask, request, render_template
import random

app = Flask(__name__)

# function to simulate a win or loss
def bet_win_lose():
    random_number = random.random()
    if random_number > 0.5:
        return True
    else:
        return False

# function to calculate the final balance after completing the wager requirement with the given multiplier
def final_balance(balance, house_edge, wager_requirement_multiplier):
    bet = balance / 10
    total_wager_needed = balance * wager_requirement_multiplier
    total_bet = 0
    bal = balance

    # simulate until the total wager needed for the given multiplier has been reached or the streamer's balance is 0
    while total_bet < total_wager_needed and bal > 0:
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

# define the number of simulations to run
simulations = 1000

# route for the input form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get the input values from the form
        balance = float(request.form['balance'])
        house_edge = float(request.form['house_edge'])
        wager_requirement_multiplier_min = float(request.form['wager_requirement_multiplier_min'])
        wager_requirement_multiplier_max = float(request.form['wager_requirement_multiplier_max'])

        # calculate the average final balance after completing the minimum wager requirement
        sum = 0
        for i in range(simulations):
            sum += final_balance(balance, house_edge, wager_requirement_multiplier_min)
        avg_balance_min = sum / simulations

        # calculate the average final balance after completing the average wager multiplier from the streamer's stats
        sum = 0
        for i in range(simulations):
            sum += final_balance(balance, house_edge, wager_requirement_multiplier_max)
        avg_balance_max = sum / simulations

        # render the results page with the calculated values
        return render_template('results.html', balance=balance, house_edge=house_edge, wager_requirement_multiplier_min=wager_requirement_multiplier_min, avg_balance_min=avg_balance_min, wager_requirement_multiplier_max=wager_requirement_multiplier_max, avg_balance_max=avg
