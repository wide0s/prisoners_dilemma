from random import choice


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
        pass

    def choose(self, choices: list, scores: list, totals: list) -> int:
        assert choices != None
        assert scores != None
        assert len(choices) == len(scores)
        assert len(totals) >= 2
        return int(self.choose0(choices, scores, totals))

    def choose0(self, choices: list, scores: list, totals: list) -> int:
        raise ShouldOverrideException(f"must override choose0()!")


class Selfish(BasePlayer):
    """
    A class representing seflish player.
    """
    def choose0(self, choices, scores, totals):
        return 0


class Coop(BasePlayer):
    """
    A class representing cooperative player.
    """

    def choose0(self, choices, scores, totals):
        return 1


class RandomChoice(BasePlayer):
    """
    A class representing player who chooses randomly.
    """

    def choose0(self, choices, scores, totals):
        return choice([0, 1])


class Pathfinder(BasePlayer):
    """
    A class representing a player who maximizes score
    when playing against egoistic and cooperative players.
    """

    def choose0(self, choices, scores, totals):
        if len(scores) < 1:
            return 1

        # outperfrom coop player
        if scores[-1] == 3 or scores[-1] == 5:
            return 0

        if scores[-1] == 0 or scores[-1] == 1:
            return 1


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

        if scores[-1] == 0:
            self._next_choice = 0

        return self._next_choice


class EyeByEye(BasePlayer):
    """
    A class representing a player copying an ally's action.
    """

    def _ally_last_choice(self, choices, scores):
        if choices[-1] == 0:
            return 1 if scores[-1] == 5 else 0
        return 1 if scores[-1] == 3 else 0


    def choose0(self, choices, scores, totals):
        if len(choices) < 1:
            return 1

        return self._ally_last_choice(choices, scores)


class AntiEyeByEye(EyeByEye):

    def choose0(self, choices, scores, totals):
        if len(choices) < 1:
            return 1

        return 1 if self._ally_last_choice(choices, scores) == 0 else 1


class Poker(BasePlayer):
    """
    A class representing a player choosing the most profitable action.
    """

    def choose0(self, choices, scores, totals):
        # warming-up
        if len(choices) < 2:
            return len(choices)

        if totals[0] > totals[1]:
            return 0
        elif totals[1] > totals[0]:
            return 1

        # should not be here
        assert totals[0] != totals[1]


class LastTwoRounds(BasePlayer):
    """
    A class representing a player choosing the best action from the last two.
    """

    def _pseudo_random_choice(self, totals):
        if totals[0] > totals[1]:
            return 0
        elif totals[1] > totals[0]:
            return 1
        return choice([0, 1])


    def choose0(self, choices, scores, totals):
        # warming-up
        if len(choices) < 2:
            return len(choices)

        if scores[-1] > scores[-2]:
            return choices[-1]
        elif scores[-2] > scores[-1]:
            return choices[-2]

        # actually both are 0
        if scores[-1] == 0:
            if choices[-1] == choices[-2]:
                return (1 - choices[-1])
            return self._pseudo_random_choice(totals)

        return choices[-1]
