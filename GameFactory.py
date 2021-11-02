import random
from collections import namedtuple
from Strategy import Game, Outcome, SimpleWin, SimpleLoss, \
    DAlembertWin, DAlembertLoss



def NewGameType(sim):
    g = Game(sim.funds, sim.initial_wager, sim.max_wagers)
    
    return g
