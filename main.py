import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple

Outcome = namedtuple('Outcome', ['wagers', 'funds', 'broke', 'profit'])
SimProperties = namedtuple('SimProperties', ['winner', 'multiple', 'bust_rate',
    'profit_rate', 'expected_value', 'roi'] )

bust_rate_required = 31.235
profit_rate_required = 63.208
graphing = False
DEBUG = 0
random_mulitple = 0


#Graphing Functions
def graph(outcomes):
    for each in outcomes:
        plt.plot(each.wagers, each.funds)
    plt.ylabel('Account Value')
    plt.xlabel('Wager Count')
    plt.axhline(0, color = 'r')

def graph_winners(winners):
    busts = []
    profits = []
    roi = []
    multiples = []
    for each in winners:
        busts.append(each.bust_rate)
        profits.append(each.profit_rate)
        roi.append(each.roi)
        multiples.append(each.multiple)

    #fig, ax = plt.subplots()

    plt.xlabel('Multiple Value')
    plt.ylabel('Profit Rate')
    #plt.plot(multiples, profits, c='k', label="Profit Rate (%)")
    plt.scatter(multiples, profits, c='k', label="Profit Rate (%)")
    plt.show()

    plt.xlabel('Multiple Value')
    plt.ylabel('Bust Rate')
    #plt.plot(multiples, busts, c='c', label="Bust Rate(%)")
    plt.scatter(multiples, busts, c='c', label="Bust Rate(%)")
    plt.show()

    plt.xlabel('Multiple Value')
    plt.ylabel('ROI Rate')
    #plt.plot(multiples, busts, c='c', label="Bust Rate(%)")
    plt.scatter(multiples, roi, c='c', label="ROI(%)")
    plt.show()


def rollDice():
    '''True player wins, False player loses'''
    roll = random.randint(1, 100)
    if roll <= 50:
        return False
    return True

def rollUnfairDice():
    '''True player wins, False player loses'''
    roll = random.randint(1, 100)
    if roll == 100:
        return False
    elif roll <= 50:
        return False
    elif 100 > roll > 50:
        return True
def multiple_bettor(funds, initial_wager, wager_count, multiple=0):
    global random_mulitple
    gamble = rollUnfairDice
    value = funds
    wager = initial_wager
    num_wagers = 1
    broke = False
    profit = False
    wX = []
    vY = []
    if multiple == 0:
        multiple = random_mulitple

    while num_wagers <= wager_count:
        if DEBUG >= 200:
            print("On wager: ", num_wagers, end="\r")
        if gamble():
            value += wager
            wager = initial_wager

        else:
            value -= wager
            wager = wager * multiple
            if (value - wager) < 0:
                wager = value

        wX.append(num_wagers)
        vY.append(value)

        num_wagers += 1
        if value <= 0:
            broke = True
            break

    if value > funds:
        profit = True

    return Outcome(wX, vY, broke, profit)

def dalembert_bettor(funds, initial_wager, wager_count, multiple=0):
    global random_mulitple
    gamble = rollDice
    value = funds
    wager = initial_wager
    num_wagers = 1
    broke = False
    profit = False
    wX = []
    vY = []

    while num_wagers <= wager_count:
        if DEBUG >= 200:
            print("On wager: ", num_wagers)
            print("Current wager: $", wager)
        if gamble():
            value += wager
            if wager <= initial_wager:
                wager = initial_wager
            else:
                wager -= initial_wager
        else:
            value -= wager
            wager += initial_wager
            if (value - wager) < 0:
                wager = value

        wX.append(num_wagers)
        vY.append(value)

        num_wagers += 1
        if value <= 0:
            broke = True
            break

    if value > funds:
        profit = True

    return Outcome(wX, vY, broke, profit)

def doubler_bettor(funds, initial_wager, wager_count):
    return multiple_bettor(funds, initial_wager, wager_count, 2)

def simple_bettor(funds, initial_wager, wager_count):
    return multiple_bettor(funds, initial_wager, wager_count, 1)

def simulation(bettor):
    global graphing, random_mulitple

    winner = False
    sample_size = 100
    starting_funds = 10000
    initial_wager = 100
    max_wagers = 100

    outcomes = []
    broke_count = 0
    profit_count = 0
    x = 0

    total_winnings = 0.0

    while x < sample_size:
        outcome = bettor(starting_funds, initial_wager, max_wagers)
        if outcome.broke:
            broke_count += 1
        if outcome.profit:
            profit_count += 1

        if len(outcome.funds) > 0:
            total_winnings += outcome.funds[-1]

        outcomes.append(outcome)
        x += 1

    total_invested      = starting_funds * sample_size
    calc_bust_rate      = broke_count*100/float(sample_size)
    calc_profit_rate    = profit_count*100/float(sample_size)
    calc_expected_value = 1.00 * total_winnings / total_invested
    calc_roi            = (total_winnings - total_invested) * 100.00 / total_invested
    if DEBUG >= 100:
        print("\ndeath rate: ", calc_bust_rate)
        print("survival rate:", 100 - calc_bust_rate)
        print("Profitability %: ", calc_profit_rate)
        print("Expected Value: ", calc_expected_value)
        print("total_winnings: ", total_winnings)
        print("total_invested: ", total_invested)
        print("ROI: ", calc_roi, "%")

    if (calc_bust_rate < bust_rate_required) and \
        (calc_profit_rate > profit_rate_required):
        winner = True
        if DEBUG >= 10:
            print("\nWINNER ##############")
            print("Random Multiple", random_mulitple)
            print("Lower bust to beat", bust_rate_required)
            print("higher profit rate to beat", profit_rate_required)
            print("bust rate", calc_bust_rate)
            print("profit rate", calc_profit_rate)
            print("Expected value per dollar: ", calc_expected_value)
            print("total_winnings: ", total_winnings)
            print("total_invested: ", total_invested)
            print("ROI: ", calc_roi, "%")


    if graphing:
        graph(outcomes)

    return outcomes, SimProperties(winner, random_mulitple, calc_bust_rate,
        calc_profit_rate, calc_expected_value, calc_roi)

def random_mulitple_simulation():
    '''Run a large number of simulations with random mulitple values
    and return a sorted list of results by success score'''
    global random_mulitple
    max_cycles  = 1000
    cycle_count = 0
    winners = []
    while cycle_count < max_cycles:
        if DEBUG > 0:
            print("Cycle: ", cycle_count, end="\r")
        random_mulitple = random.uniform(0.1, 10.0)
        outcomes, props = simulation(multiple_bettor)
        if props.winner:
            winners.append(props)
        cycle_count += 1

    by_profit_rate = sorted(winners, key=lambda x: x.profit_rate, reverse=True)
    num_top_winners = min(5, len(winners))
    print("#Top 5 Winners sorted by Profit Rate#")
    for x in range(0, num_top_winners):
        print_winner(by_profit_rate[x])

    print("#Top 5 Winners sorted by Bust Rate#")
    by_bust_rate = sorted(winners, key=lambda x: x.bust_rate)
    for x in range(0, num_top_winners):
        print_winner(by_bust_rate[x])

    print("#Top 5 Winners sorted by ROI#")
    by_roi = sorted(winners, key=lambda x: x.roi, reverse = True)
    for x in range(0, num_top_winners):
        print_winner(by_roi[x])

    graph_winners(winners)

def print_winner(winner):
        print("#########")
        print("Multiple: ", winner.multiple)
        print("Profit Rate: ", winner.profit_rate)
        print("Bust Rate: ", winner.bust_rate)
        print("ROI: ", winner.roi)
        print("Expected Value: ", winner.expected_value)
        print()

def main():
    global graphing, DEBUG
    graphing = False
    DEBUG = 0
    # simulation(simple_bettor)
    # simulation(doubler_bettor)
    random_mulitple_simulation()
    # simulation(dalembert_bettor)


    if graphing:
         plt.show()


if __name__ == '__main__':
    main()
