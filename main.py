#!/usr/bin/python3

import argparse
from tabulate import tabulate

from factory import PlayerFactory
from games import GameOfTwo


def main(args):
    n_rounds = args.rounds
    verbose = args.v

    print(f"ROUNDS={n_rounds}")

    data_aggr = []
    data_matrix = []
    player_names = PlayerFactory.class_names()
    for player1_class_name in player_names:
        row = [player1_class_name]
        player1_total_score = 0
        for player2_class_name in player_names:
            player1 = PlayerFactory.get(player1_class_name)()
            player2 = PlayerFactory.get(player2_class_name)()
            game = GameOfTwo(player1, player2)
            for _round in range(n_rounds):
                game.play()
            scr1 = game.total_scores1
            scr2 = game.total_scores2
            if verbose:
                print(f"{game.name()}: {scr1[-1]} ({scr1[0]}, {scr1[1]}) \ {scr2[-1]} ({scr2[0]}, {scr2[1]})")
            row.append(f"{scr1[-1]} \ {scr2[-1]}")
            player1_total_score += scr1[-1]
        data_matrix.append(row)
        data_aggr.append([player1_class_name, player1_total_score, player1_total_score / len(player_names), 
            player1_total_score / len(player_names) / n_rounds])

    print(tabulate(tuple(data_matrix), headers=['      \       '] + player_names))
    print('\n' + tabulate(tuple(sorted(data_aggr, key = lambda x: x[1], reverse=True)), \
            headers=['', 'SCORE', 'AVERAGE PER GAME', 'AVERAGE PER ROUND']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game of Two')
    parser.add_argument(
            '-r',
            '--rounds',
            type=int,
            default=1000,
            help='number of rounds (default: 1000)'
    )
    parser.add_argument('-v', action='store_true', default=False, help='verbose output')
    main(parser.parse_args())
