import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple

Outcome = namedtuple('Outcome', ['wagers', 'funds', 'broke', 'profit'])
SimProperties = namedtuple('SimProperties', ['winner', 'multiple', 'bust_rate', 'profit_rate'] )

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
    multiples = []
    for each in winners:
        busts.append(each.bust_rate)
        profits.append(each.profit_rate)
        multiples.append(each.multiple)

    #fig, ax = plt.subplots()

    plt.xlabel('Multiple Value')
    plt.ylabel('Profit Rate')
    plt.scatter(multiples, profits, c='k', label="Profit Rate (%)")
    plt.show()

    plt.xlabel('Multiple Value')
    plt.ylabel('Bust Rate')
    plt.scatter(multiples, busts, c='c', label="Bust Rate(%)")
    plt.show()


def rollDice():
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
        if DEBUG > 100:
            print("On wager: ", num_wagers, end="\r")
        if rollDice():
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
    value = funds
    wager = initial_wager
    num_wagers = 1
    broke = False
    profit = False
    wX = []
    vY = []

    while num_wagers <= wager_count:
        if DEBUG > 100:
            print("On wager: ", num_wagers, end="\r")
        if rollDice():
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

    while x < sample_size:
        outcome = bettor(starting_funds, initial_wager, max_wagers)
        if outcome.broke:
            broke_count += 1
        if outcome.profit:
            profit_count += 1
        outcomes.append(outcome)
        x += 1

    calc_bust_rate = broke_count*100/float(sample_size)
    calc_profit_rate = profit_count*100/float(sample_size)

    if DEBUG > 100:
        print("\ndeath rate: ", calc_bust_rate)
        print("survival rate:", 100 - calc_bust_rate)
        print("Profitability %: ", calc_profit_rate)

    if (calc_bust_rate < bust_rate_required) and \
        (calc_profit_rate > profit_rate_required):
        winner = True
        if DEBUG > 10:
            print("\nWINNER ##############")
            print("Random Multiple", random_mulitple)
            print("Lower bust to beat", bust_rate_required)
            print("higher profit rate to beat", profit_rate_required)
            print("bust rate", calc_bust_rate)
            print("profit rate", calc_profit_rate)
    # else:
    #     print("\Loser :( ##############")
    #     print("Random Multiple", random_mulitple)
    #     print("Lower bust to beat", bust_rate_required)
    #     print("higher profit rate to beat", profit_rate_required)
    #     print("bust rate", calc_bust_rate)
    #     print("profit rate", calc_profit_rate)

    if graphing:
        graph(outcomes)

    return outcomes, SimProperties(winner, random_mulitple, calc_bust_rate, calc_profit_rate)

def random_simulation():
    '''Run a large number of random simulations
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
        print("#########")
        print("Multiple: ", by_profit_rate[x].multiple)
        print("Profit Rate: ", by_profit_rate[x].profit_rate)
        print("Bust Rate: ", by_profit_rate[x].bust_rate)

    print("#Top 5 Winners sorted by Bust Rate#")
    by_bust_rate = sorted(winners, key=lambda x: x.bust_rate)
    for x in range(0, num_top_winners):
        print("#########")
        print("Multiple: ", by_bust_rate[x].multiple)
        print("Profit Rate: ", by_bust_rate[x].profit_rate)
        print("Bust Rate: ", by_bust_rate[x].bust_rate)

    graph_winners(winners)


def main():
    global graphing, DEBUG
    graphing = True
    DEBUG = 0
    # simulation(simple_bettor)
    # simulation(doubler_bettor)
    # random_simulation()
    simulation(dalembert_bettor)


    if graphing:
         plt.show()


if __name__ == '__main__':
    main()
