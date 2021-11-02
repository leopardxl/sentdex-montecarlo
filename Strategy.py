from collections import namedtuple
import random

Outcome = namedtuple('Outcome', ['wagers', 'funds', 'broke', 'profit'])

def rollUnfairDice():
    '''True player wins, False player loses'''
    roll = random.randint(1, 100)
    if roll == 100:
        return False
    elif roll <= 50:
        return False
    elif 100 > roll > 50:
        return True
def rollDice():
    '''True player wins, False player loses'''
    roll = random.randint(1, 100)
    if roll <= 50:
        return False
    return True

def SimpleLoss(state):
    state.value -= state.wager
    state.wager = state.wager * state.multiple
    if (state.value - state.wager) < 0:
        state.wager = state.value
def SimpleWin(state):
    state.value += state.wager
    state.wager = state.initial_wager

def DAlembertWin(state):
    state.value += state.wager
    if state.wager <= state.initial_wager:
        state.wager = state.initial_wager
    else:
        state.wager -= state.initial_wager

def DAlembertLoss(state):
    self.value -= self.wager
    self.wager += self.initial_wager
    if (self.value - self.wager) < 0:
        self.wager = self.value


class Game:
    def __init__(self, funds, initial_wager, wager_count):
        self.multiple = 1
        self.initial_funds = funds
        self.value = funds
        self.initial_wager = initial_wager
        self.wager = initial_wager
        self.num_wagers = 0
        self.wager_count = wager_count
        self.broke = False
        self.profit = False
        self.wX = []
        self.vY = []
        self.gamble = rollUnfairDice
        self.won_round = SimpleWin
        self.lost_round = SimpleLoss

    def play(self):
        while self.num_wagers <= self.wager_count:
            if self.gamble():
                self.won_round(self)
            else:
                self.lost_round(self)

            self.wX.append(self.num_wagers)
            self.vY.append(self.value)

            self.num_wagers += 1
            if self.value <= 0:
                self.broke = True
                break

        if self.value > self.initial_funds:
            self.profit = True

        return Outcome(self.wX, self.vY, self.broke, self.profit)

if __name__ == '__main__':

    starting_funds = 10000
    initial_wager = 100
    max_wagers = 100
    simple = Game(starting_funds, initial_wager, max_wagers)
    simple.multiple = 2
    out = simple.play()
    print(simple.wX)
    print(simple.vY)
