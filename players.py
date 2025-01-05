from random import choice
from typing import Tuple, Union

EXCLUDE_PLAYERS = []


class ShouldOverrideException(Exception):
    pass


class BasePlayer:
    """
    A base class representing a player.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self._random = None

    def set_random(self, _random = None):
        self._random = _random

    def random_choice(self, seq: list):
        if self._random is not None:
            return self._random.choice(seq)
        return choice(seq)

    def choose(self, choices: list, scores: list, totals: list, oppo_choices: list, oppo_scores: list, oppo_totals: list) -> int:
        assert choices != None and oppo_choices != None
        assert scores != None and oppo_scores != None
        assert len(choices) == len(scores) and len(oppo_choices) == len (oppo_scores)
        assert len(totals) >= 2 and len(oppo_totals) >= 2
        return int(self.choose0(choices, scores, totals, oppo_choices, oppo_scores, oppo_totals))

    def choose0(self, choices: list, scores: list, totals: list,
            oppo_choices: list, oppo_scores: list, oppo_totals: list) -> int:
        raise ShouldOverrideException(f"must override choose0()!")


class Selfish(BasePlayer):
    """
    A class representing seflish player.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        return 0


class Cooperative(BasePlayer): # former name: Coop
    """
    A class representing always cooperative player.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        return 1


class RandomChoice(BasePlayer):
    """
    A class representing player who chooses randomly.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        return self.random_choice([0, 1])


class Pathfinder1(BasePlayer): # former name: Pathfinder
    """
    A class representing a player trying to earn more than in
    the previous round.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        if len(scores) < 1:
            return 1

        if scores[-1] == 3 or scores[-1] == 5: # (1, 1) or (0, 1) -> (0, x)
            return 0

        if scores[-1] == 0 or scores[-1] == 1: # (1, 0) or (0, 0) -> (1, x)
            return 1


class Pathfinder0(Pathfinder1): # former name: Pathfinder2
    """
    A class that represents Pathfinder strategy, but starts
    with 0 (deception). It almost always beats Pathfinder1.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        if len(scores) < 1:
            return 0 # 0 significantly improves performance
        return super().choose0(choices, scores, totals,  oppo_choices, oppo_scores,
                oppo_totals)


class Pedantic(BasePlayer):

    def reset(self):
        super().reset()
        self._random_rounds = 10


    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        # warming-up
        if (len(choices) + 1) < self._random_rounds:
            return self.random_choice([0, 1])

        if totals[0] > totals[1]:
            return 0
        return 1


class Friedman(BasePlayer):
    """
    A class representing a player who cooperates until the 
    first betrayal - then it always betrays.
    """

    def reset(self):
        super().reset()
        self._next_choice = 1


    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        if len(choices) < 1:
            return 1

        if oppo_choices[-1] == 0:
            self._next_choice = 0

        return self._next_choice


class EyeByEye(BasePlayer):
    """
    A class representing a player who chooses the same action as the
    opponent's last choice.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        if len(choices) < 1:
            return 1
        return oppo_choices[-1]


class AntiEyeByEye(BasePlayer):
    """
    A class representing a player who chooses the opposite action to
    its opponent's last action.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        if len(choices) < 1:
            return 1
        return 1 - oppo_choices[-1]


class Poker(BasePlayer):
    """
    A class representing a player choosing the most profitable action.
    TODO:
     1. to try the initial steps in reverse order
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        # warming-up: tries 0, then 1
        if len(choices) < 2:
            return len(choices)

        if totals[0] > totals[1]:
            return 0
        elif totals[1] > totals[0]:
            return 1

        # should not be here
        assert totals[0] == totals[1]


class PokerAggr(BasePlayer):
    """
    A class representing a player choosing ...
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        # warming-up: tries 0, then 1
        if len(choices) < 2:
            return len(choices)

        aggr_totals = [totals[idx] + oppo_totals[idx] for idx in range(0, 2)]

        if aggr_totals[0] > aggr_totals[1]:
            return 0
        elif aggr_totals[1] > aggr_totals[0]:
            return 1

        # TODO: think twice what to return
        return choices[-1]


class LastTwoRounds(BasePlayer):
    """
    A class representing a player choosing the best action from the last two.

    TODO:
     1. to try the initial steps in reverse order
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        # warming-up: tries 0, then 1
        if len(choices) < 2:
            return len(choices)

        if scores[-1] > scores[-2]:
            return choices[-1]
        elif scores[-2] > scores[-1]:
            return choices[-2]

        # actually both are 0
        if scores[-1] == 0:
            return 0

        return choices[-1]


class BestOfLastTwo(BasePlayer): # former name: LastTwoRoundsV2
    """
    A class representing a player who chooses the action that
    brought the highest total number of points in two previous
    rounds.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        # warming-up: tries 0, then 1
        if len(choices) < 2:
            return len(choices) # always wins {1, 0}

        round_scores = [scores[idx - 2] + oppo_scores[idx - 2] for idx in range(0, 2)]

        if round_scores[-1] > round_scores[-2]:
            return choices[-1]
        elif round_scores[-2] > round_scores[-1]:
            return choices[-2]

        return self.default_choice(choices)

    def default_choice(self, choices):
        return 1 # same result if return choice[-1]; 1 always wins choice[-2]
                 # and choice([choices[-2], choices[-1])


class Periodic110(BasePlayer):
    """
    A class representing a player who chooses {0,1,1,0,1,1,0,1,1...}.
    """

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        # warming-up: tries 0, then 1
        if len(choices) < 2:
            return len(choices)

        if (choices[-2] + choices[-1]) == 1:
            return 1
        if choices[-1] == 1:
            return 0
        # reachable if starts from {0,0, ...}
        return 1
