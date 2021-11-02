import random
from collections import namedtuple
from Strategy import Game, Outcome, SimpleLoss, SimpleWin, DAlembertWin, DAlembertLoss
import matplotlib.pyplot as plt

Outcome = namedtuple('Outcome', ['wagers', 'funds', 'broke', 'profit'])
SimProperties = namedtuple('SimProperties', ['winner', 'multiple', 'bust_rate',
    'profit_rate', 'expected_value', 'roi'] )


class Simulation:
    def __init__(self):
        self.game= None
        self.sample_size = 100
        self.funds = 10000
        self.initial_wager = 100
        self.max_wagers = 100

        self.outcomes = []
        self.broke_count = 0
        self.profit_count = 0
        self.bust_rate_required = 31.235
        self.profit_rate_required = 63.208
        self.total_winnings = 0.0

        self.total_invested = self.funds * self.sample_size
        self.bust_rate      = 0
        self.profit_rate    = 0
        self.expected_value = 0
        self.roi            = 0
        self.winner = False



    def set_game(self, game):
        self.game = game

    def run(self):
        broke_count = 0
        profit_count = 0
        x = 0
        while x < self.sample_size:
            outcome = self.play_game()
            if outcome.broke:
                broke_count += 1
            if outcome.profit:
                profit_count += 1

            if len(outcome.funds) > 0:
                self.total_winnings += outcome.funds[-1]

            self.outcomes.append(outcome)
            x += 1

        total_invested      = self.funds * self.sample_size
        self.bust_rate      = broke_count*100/float(self.sample_size)
        self.profit_rate    = profit_count*100/float(self.sample_size)
        self.expected_value = 1.00 * self.total_winnings / total_invested
        self.roi            = (self.total_winnings - total_invested) * 100.00 / total_invested
        if (self.bust_rate < self.bust_rate_required) and \
            (self.profit_rate > self.profit_rate_required):
            self.winner = True

    def play_game(self):
        # TODO: Add various game creation logic here
        g = Game(self.funds, self.initial_wager, self.max_wagers)
        return g.play()

    def graph(self):
        print(len(self.outcomes))
        #print(self.outcomes)
        for each in self.outcomes:
            plt.plot(each.wagers, each.funds)
        plt.ylabel('Account Value')
        plt.xlabel('Wager Count')
        plt.axhline(0, color = 'r')
        plt.show()

if __name__ == '__main__':
    sim = Simulation()
    sim.run()
    sim.graph()
