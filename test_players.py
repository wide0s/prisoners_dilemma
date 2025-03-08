from factory import PlayerFactory
from players import BasePlayer
from games import PrisonersDilemma


class Puppet(BasePlayer):
    """
    A puppet.
    """

    def __init__(self, choices):
        super().__init__()
        self._choices = choices
        self._index = -1

    def choose0(self, choices, scores, totals, oppo_choices, oppo_scores, oppo_totals):
        self._index += 1
        return self._choices[self._index]

vectors = [
        "Friedman", [1,1,0,1,1,1,1,1,1,1,1], [1,1,1,0,0,0,0,0,0,0,0],
        "SoftFriedman", [1,0,1,0,1,0,0,1,1,0,1,0,0] + [1] * 10, [1,1,1,1,1,1,1,1,1,1,1,1,1] + [0] * 10,
        "TitForTat", [1,0,1,0,1,0,1,1,1], [1,1,0,1,0,1,0,1,1]
        ]

for i in range(0, len(vectors), 3):
    player_name = vectors[i] 
    player = PlayerFactory.get(player_name)()
    puppet = Puppet(vectors[i + 1])
    expected = vectors[i + 2]
    game = PrisonersDilemma(player, puppet)
    rounds = len(puppet._choices)
    print(f"{game.name()}, {rounds} rounds")
    for _ in range(rounds):
        game.play()
    assert expected == game.choices1, \
            f'for {player_name} and opponent\'s choices {puppet._choices} expected answers are {expected}, while got {game.choices1}'
