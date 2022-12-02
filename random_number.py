import random

initial_balance = 10000
house_edge = 0.1
wager_requirement_multiplier_min = 5
wager_requirement_multiplier_max = 10

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

print("Starting balance: " + str(initial_balance))
print("House edge: " + str(house_edge))
print("Wager requirement multiplier: " + str(wager_requirement_multiplier_min))
print("Average wager multiplier from stats if they are degen: " + str(wager_requirement_multiplier_max))

final_balance_min = simulate_bets(initial_balance, house_edge, wager_requirement_multiplier_min, simulations)
print(f"The final balance after a {wager_requirement_multiplier_min}x wager requirement: {final_balance_min}")

final_balance_max = simulate_bets(initial_balance, house_edge, wager_requirement_multiplier_max, simulations)
print(f"The final balance after a {wager_requirement_multiplier_max}x wager requirement since the streamer played over the minimum: {final_balance_max}")
