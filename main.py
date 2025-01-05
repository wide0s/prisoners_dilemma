#!/usr/bin/python3

import argparse
from os import urandom
from random import Random
from tabulate import tabulate

from factory import PlayerFactory
from games import GameOfTwo


def main(args):
    rounds = args.rounds

    print(f"ROUNDS={rounds}")

    player_names = PlayerFactory.class_names()
    prng_seeds = {} if not args.s else \
            { k:int.from_bytes(urandom(8), byteorder='big') for k in player_names }
    raw_results = [ [n] + [0] * len(player_names) for n in player_names ]
    for row, player1_name in enumerate(player_names):
        for column, player2_name in enumerate(player_names[row:]):
            player1 = PlayerFactory.get(player1_name)()
            player2 = PlayerFactory.get(player2_name)()
            if prng_seeds.get(player1_name) is not None:
                player1.set_random(Random(prng_seeds.get(player1_name)))
            if prng_seeds.get(player2_name) is not None:
                player2.set_random(Random(prng_seeds.get(player2_name)))
            game = GameOfTwo(player1, player2)
            for _ in range(rounds):
                game.play()
            total1 = game.total_scores1
            total2 = game.total_scores2
            if args.v:
                print(f"{game.name()}: {total1[-1]} (0={total1[0]}, 1={total1[1]}) \ {total2[-1]} (0={total2[0]}, 1={total2[1]})")
            raw_results[row][1 + row + column] = [total1, total2]
            raw_results[row + column][1 + row] = [total2, total1]

    p2p_tab = [] # points earned by players in a game
    player_tab = [] # player points earned in all games
    winner_tab = [] # points earned in all games with a specific player 
    for row in raw_results:
        p2p_row = [row[0]] # player name
        player_total = game_total = 0
        for column in row[1:]:
            p2p_row.append(f"{column[0][-1]} \ {column[1][-1]}")
            player_total += column[0][-1]
            game_total += column[0][-1] + column[1][-1]
        p2p_tab.append(p2p_row)
        player_tab.append([row[0], player_total, player_total / len(player_names), player_total / len(player_names) / rounds])
        winner_tab.append([row[0], game_total, game_total / len(player_names), game_total / len(player_names) / rounds])

    print(tabulate(tuple(p2p_tab), headers=['      \       '] + player_names))
    print('\n' + tabulate(tuple(sorted(player_tab, key = lambda x: x[1], reverse=True)), \
            headers=['', 'PLAYER SCORE', 'AVERAGE PER GAME', 'AVERAGE PER ROUND']))
    print('\n' + tabulate(tuple(sorted(winner_tab, key = lambda x: x[1], reverse=True)), \
            headers=['', 'GAME SCORE', 'AVERAGE PER GAME', 'AVERAGE PER ROUND']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game of Two')
    parser.add_argument(
            '-r',
            '--rounds',
            type=int,
            default=1000,
            help='number of rounds (default: 1000)'
    )
    parser.add_argument('-v', action='store_true', default=False, help='verbose output (default: False)')
    parser.add_argument('-s', action='store_true', default=False, help='player uses the same PRNG seed (default: False)')
    main(parser.parse_args())
