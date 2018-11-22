import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple

Outcome = namedtuple('Outcome', ['wagers', 'funds', 'broke'])

def rollDice():
    roll = random.randint(1, 100)
    if roll == 100:
        #print(roll, ", role was 100, you lose")
        return False
    elif roll <= 50:
        #print(roll, ", role was 1-50, you lose")
        return False
    elif 100 > roll > 50:
        #print(roll, ", role was 51-99, you win")
        return True

def doubler_better(funds, initial_wager, wager_count):
    value = funds
    wager = initial_wager
    num_wagers = 1
    broke = False
    wX = []
    vY = []

    prevWin = True
    prevWagerAmount = wager

    while num_wagers <= wager_count:
        prevWagerAmount = wager
        if rollDice():
            value += wager
            prevWin = True
            wager = initial_wager

        else:
            value -= wager
            privWin = False
            wager = wager * 2

        wX.append(num_wagers)
        vY.append(value)

        num_wagers += 1
        if value < 0:
            broke = True
            break


    return Outcome(wX, vY, broke)

def simple_bettor(funds, initial_wager, wager_count):
    value = funds
    wager = initial_wager
    num_wagers = 1
    broke = False
    wX = []
    vY = []

    while num_wagers <= wager_count:
        if rollDice():
            value += wager
        else:
            value -= wager

        wX.append(num_wagers)
        vY.append(value)
        num_wagers += 1
        if value < 0:
            broke = True
            break


    return Outcome(wX, vY, broke)



def graph(outcomes):
    for each in outcomes:
        plt.plot(each.wagers, each.funds)
    plt.ylabel('Account Value')
    plt.xlabel('Wager Count')
    plt.axhline(0, color = 'r')
    plt.show()


def main():
    outcomes = []
    broke_count = 0
    x = 0
    while x < 1000:
        outcome = simple_bettor(10000, 100, 10000)
        #outcome = doubler_better(10000, 100, 100)
        if outcome.broke:
            broke_count += 1

        outcomes.append(outcome)
        x += 1
    print("death rate: ", broke_count*100/float(x) )
    print("survival rate:", 100 -  broke_count*100/float(x) )
    graph(outcomes)

if __name__ == '__main__':
    main()
