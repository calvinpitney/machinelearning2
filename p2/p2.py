#!/usr/bin/env python3

# Calvin Pitney
# 7.3.18
# CMSC 421- Brule

import sys
import random
import collections
import copy

# Reward for mutual cooperation
CC_REWARD = 3

# Reward for cooperating, when the other player defects
CD_REWARD = 0

# Reward for defecting, when the other player cooperates
DC_REWARD = 4

# Reward for mutual defection
DD_REWARD = 1


# Bots

class TFTBot:
    """
    Plays Tit for Tat strategy, initally cooperating

    play_count is unused, but provides an example how to initialize
    instance variables in Python
    """

    def __init__(self):
        self.rounds_played = 0

    def play(self, prev):
        """
        prev refers to the other player's previous action; for the first
        action of a repeated game, prev will be None
        """
        self.rounds_played += 1
        if prev == "D":
            return "D"
        else:
            return "C"

    def reset(self):
        """
        Reset instance variables (call before each game of iterated
        prisoner's dilemma)
        """
        self.rounds_played = 0


class CooperateBot:
    """Always cooperates"""
    def __init__(self):
        pass

    def play(self, prev):
        return "C"

    def reset(self):
        pass


class DefectBot:
    """Always defects"""
    def __init__(self):
        pass

    def play(self, prev):
        return "D"

    def reset(self):
        pass


class RandomBot:
    """"Plays randomly (equal probability)"""
    def __init__(self):
        pass

    def play(self, prev):
        if random.uniform(0, 1) > 0.5:
            return "C"
        else:
            return "D"

    def reset(self):
        pass


class GrudgeBot:
    """

    GrudgeBot will cooperate in IPD until the other player defects,
    after which GrudgeBot will always defect
    """
    def __init__(self):
        self.defect = 0

    def play(self, prev):
        if self.defect == 0:
            if prev == "D":
                self.defect = 1
                return "D"
            return "C"
        else:
            return "D"

    def reset(self):
        self.defect = 0


class ForgivingBot:
    """
    ForgivingBot will cooperate, unless the other player has defected
    in the previous two rounds (also known as "Tit for two tats")
    """
    def __init__(self):
        self.defects = 0

    def play(self, prev):
        if prev == "D":
            self.defects += 1
        else:
            self.defects = 0
        if self.defects > 1:
            return "D"
        else:
            return "C"

    def reset(self):
        self.defects = 0


class StudentBot:
    """
    TODO: Implement

    Implement a custom IPD agent
    """
    def __init__(self):
        self.student_name = "Calvin Pitney"

    def play(self, prev):
        r = random.uniform(0,1)
        if r > 0.3 and prev == "D":
            return "D"
        elif prev == "C":
            return "C"
        else:
            return "D"

    def reset(self):
        pass


# Some helper functions

def duplicate_bot(old_bot):
    """Return a new instance of old_bot's class"""
    return old_bot.__class__()


def name_of_bot(bot):
    """Return the name of bot's class"""
    return bot.__class__.__name__


def count_bots(bots):
    """Count the number of each type of bot in a list of bots"""
    return dict(collections.Counter([name_of_bot(b) for b in bots]))


# TODO: implement play_ipd, play_tournament, evolutionary_ipd

def play_ipd(bot1, bot2, rounds, noise=0.0):
    """
    Play iterated prisoner's dilemma between bot1 and bot2

    rounds - number of rounds
    noise - probability that a bot performs the OPPOSITE of its intended
            action; by default, this probability is zero

    Return (a, b) where a is total utility of bot1, b is total utility bot2
    """
    a, b, x1, x2, y1, y2 = play_ipd_r(bot1, bot2, rounds, noise)
    return (a,b)

def play_ipd_r(bot1, bot2, rounds, noise=0.0):
    if rounds > 1:
        utility = play_ipd_r(bot1, bot2, rounds-1, noise)
        b1 = bot1.play(utility[5])
        if random.uniform(0, 1) < noise:
            if b1 == "C":
                b1 = "D"
            else:
                b1 = "C"
        b2 = bot2.play(utility[4])
        if random.uniform(0, 1) < noise:
            if b2 == "C":
                b2 = "D"
            else:
                b2 = "C"
        if b1 == "C":
            if b2 == "C":
                return (utility[0]+3, utility[1]+3, bot1, bot2, b1, b2)
            else:
                return (utility[0], utility[1]+4, bot1, bot2, b1, b2)
        else:
            if b2 == "C":
                return (utility[0]+4, utility[1], bot1, bot2, b1, b2)
            else:
                return (utility[0]+1, utility[1]+1, bot1, bot2, b1, b2)
    else:
        b1 = bot1.play("")
        b2 = bot2.play("")
        if random.uniform(0, 1) < noise:
            if b1 == "C":
                b1 = "D"
            else:
                b1 = "C"
        if random.uniform(0, 1) < noise:
            if b2 == "C":
                b2 = "D"
            else:
                b2 = "C"
        if b1 == "C":
            if b2 == "C":
                return (3,3, bot1, bot2, b1, b2)
            else:
                return (0,4, bot1, bot2, b1, b2)
        else:
            if b2 == "C":
                return (4,0, bot1, bot2, b1, b2)
            else:
                return (1,1, bot1, bot2, b1, b2)




    return (0, 0)


def play_tournament(bots, rounds, noise=0.0):
    """
    Play a round-robin IPD tournament
    Every bot plays every other bot exactly once
    Bots DO NOT play against themselves.

    bots - list of bot objects
    rounds - number of rounds in IPD
    Return list of (utility, bot), where utility is the total utiltiy
    and bot is the Bot object, e.g. 
    [(10, <CooperateBot instance at 0x...), ...
    """
    results = []
    numBots = len(bots)
    utilResult = [0] * numBots
    for x in range(0,numBots):
        for y in range(0,numBots):
            if y > x:
                utilBx, utilBy = play_ipd(bots[x], bots[y], rounds, noise)
                utilResult[x] += utilBx
                utilResult[y] += utilBy

    for z in range(0,numBots):
        results.append((utilResult[z], bots[z]))
    return results


def evolutionary_ipd(bots, rounds, generations, noise=0.0):
    """
    Play an IPD tournament for a given number of rounds

    At the end, the two highest scoring bots get duplicated; the two
    lowest scoring bots get removed. This becomes a 'new generation'.
    Repeat this process for a given number of 'generations'

    bots - list of bot objects
    rounds - number of rounds for each iterated prisoner's dilemma
    generations - number of tournaments to play; each tournament
                  constitutes a 'generation'

    Return the last generation (a list of bot objects)
    """
    bots_return = bots
    num_bot = len(bots)

    for x in range(0, generations - 1):
        round_results = play_tournament(bots_return, rounds, noise)
        round_results.sort()
        best = round_results[num_bot-1]
        secondBest = round_results[num_bot-2]
        round_results.pop(0)
        round_results.pop(0)
        round_results.insert(len(round_results), copy.copy(secondBest))
        round_results.insert(len(round_results), copy.copy(secondBest))
        bots_return = []
        for y in range(len(round_results)):
            bots_return.append(round_results[y][1])
    return bots_return


def main():
    """Example: play evolutionary IPD with different noise levels"""

    # Initial population is 5 Cooperate, Defect and TFT Bots
    population = ([CooperateBot() for i in range(5)] + 
        [DefectBot() for i in range(5)] + [TFTBot() for i in range(5)])
    
    # Low noise; favors CooperateBot and TFTBot
    print(count_bots(evolutionary_ipd(population, 10, 20, 0.05)))

    # Medium noise
    print(count_bots(evolutionary_ipd(population, 10, 20, 0.1)))

    # High noise; favors DefectBot
    print(count_bots(evolutionary_ipd(population, 10, 20, 0.25)))


if __name__ == "__main__":
    main()

