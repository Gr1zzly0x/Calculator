from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get user-entered values
        initial_balance = request.form['initial_balance']
        house_edge = request.form['house_edge']
        wager_requirement_multiplier_min = request.form['wager_requirement_multiplier_min']
        wager_requirement_multiplier_max = request.form['wager_requirement_multiplier_max']

        # simulate bets
        def simulate_bets(initial_balance, house_edge, wager_requirement_multiplier, simulations):
            balance = initial_balance
            bet = balance / 10
            total_wager_needed = balance * wager_requirement_multiplier

            def bet_win_lose():
                return random.random() > 0.5

            def final_balance():
                total_bet = 0
                bal = balance

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

            sum = 0
            for _ in range(simulations):
                sum += final_balance()

            return sum / simulations

        simulations = 100000

        # calculate final balance
        final_balance_min = simulate_bets(initial_balance, house_edge, wager_requirement_multiplier_min, simulations)
        final_balance_max = simulate_bets(initial_balance, house_edge, wager_requirement_multiplier_max, simulations)

        # render HTML template and pass in variables
        return render_template('index.html', initial_balance=initial_balance, house_edge=house_edge,
                               wager_requirement_multiplier_min=wager_requirement_multiplier_min,
                               final_balance_min=final_balance_min,
                               wager_requirement_multiplier_max=wager_requirement_multiplier_max,
                               final_balance_max=final_balance_max)

    # display form for user input
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
