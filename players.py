from random import choice


EXCLUDE_PLAYERS = ['Pathfinder*']


class ShouldOverrideException(Exception):
    pass


class BasePlayer:
    """
    A base class representing a player.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        pass

    def choose(self, choices: list, scores: list, totals: list) -> int:
        assert choices != None
        assert scores != None
        assert len(choices) == len(scores)
        assert len(totals) >= 2
        return int(self.choose0(choices, scores, totals))

    def choose0(self, choices: list, scores: list, totals: list) -> int:
        raise ShouldOverrideException(f"must override choose0()!")

    def opponent_last_choice(self, scores: list, inverse = False) -> int:
        choice = 0 if scores[-1] == 1 or scores[-1] == 0 else 1
        return 1 - choice if inverse else choice


class Selfish(BasePlayer):
    """
    A class representing seflish player.
    """
    def choose0(self, choices, scores, totals):
        return 0


class Coop(BasePlayer):
    """
    A class representing always cooperative player.
    """

    def choose0(self, choices, scores, totals):
        return 1


class RandomChoice(BasePlayer):
    """
    A class representing player who chooses randomly.
    """

    def choose0(self, choices, scores, totals):
        return choice([0, 1])


class Pathfinder1(BasePlayer):
    """
    A class representing a player trying to earn more than in
    the previous round.
    """

    def choose0(self, choices, scores, totals):
        if len(scores) < 1:
            return 1

        if scores[-1] == 3 or scores[-1] == 5: # (1, 1) or (0, 1) -> (0, x)
            return 0

        if scores[-1] == 0 or scores[-1] == 1: # (1, 0) or (0, 0) -> (1, x)
            return 1


class Pathfinder0(Pathfinder1): # previous name: Pathfinder2
    """
    A class that represents Pathfinder strategy, but starts
    with 0 (deception). It almost always beats Pathfinder1.
    """


    def choose0(self, choices, scores, totals):
        if len(scores) < 1:
            return 0 # 0 significantly improves performance
        return super().choose0(choices, scores, totals)


class Pedantic(BasePlayer):

    def reset(self):
        super().reset()
        self._random_rounds = 10


    def choose0(self, choices, scores, totals):
        # warming-up
        if (len(choices) + 1) < self._random_rounds:
            return choice([0, 1])

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


    def choose0(self, choices, scores, totals):
        if len(choices) < 1:
            return 1

        if self.opponent_last_choice(scores) == 0:
            self._next_choice = 0

        return self._next_choice


class EyeByEye(BasePlayer):
    """
    A class representing a player who chooses the same action as the
    opponent's last choice.
    """

    def choose0(self, choices, scores, totals):
        if len(choices) < 1:
            return 1
        return self.opponent_last_choice(scores)


class AntiEyeByEye(BasePlayer):
    """
    A class representing a player who chooses the opposite action to
    its opponent's last action.
    """

    def choose0(self, choices, scores, totals):
        if len(choices) < 1:
            return 1
        return self.opponent_last_choice(scores, inverse=True)


class Poker(BasePlayer):
    """
    A class representing a player choosing the most profitable action.
    TODO:
     1. to try the initial steps in reverse order
    """

    def choose0(self, choices, scores, totals):
        # warming-up: tries 0, then 1
        if len(choices) < 2:
            return len(choices)

        if totals[0] > totals[1]:
            return 0
        elif totals[1] > totals[0]:
            return 1

        # should not be here
        assert totals[0] == totals[1]


class LastTwoRounds(BasePlayer):
    """
    A class representing a player choosing the best action from the last two.

    TODO:
     1. to try the initial steps in reverse order
    """

    def choose0(self, choices, scores, totals):
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
