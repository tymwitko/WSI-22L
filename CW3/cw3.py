# Tymon Kobylecki WSI 22L

from cmath import inf
import copy
from two_player_games.player import Player
from two_player_games.move import Move
from two_player_games.state import State
from two_player_games.game import Game
from two_player_games.games.connect_four import ConnectFour, ConnectFourMove, ConnectFourState

def heuristic_val(node):
    return 0 # TODO

def is_terminal(node): #
    return node.is_finished()

def alpha_beta(board, depth , a , b , maximizingPlayer, max_turn, game): # Board jest typu ConnectFourState
    if depth == 0 or is_terminal(board):
        return heuristic_val(board), None
    moves = board.get_moves()
    best_move = None
    if max_turn:
        value = -inf
        for move in moves:
            boardcopy = copy.deepcopy(board)
            boardcopy.make_move(move)
            alpbet = alpha_beta( boardcopy , depth-1 , a , b , maximizingPlayer, not max_turn, game)[0]
            if alpbet > value:
                best_move = move
            value = max (value , alpbet)
            a = max(a , value)
            if value >= b:
                break #( * b c u t o f f * )
        return value, best_move
    else:
        value = inf
        for move in moves:
            boardcopy = copy.deepcopy(board)
            boardcopy.make_move(move)
            alpbet = alpha_beta( boardcopy , depth-1 , a , b , maximizingPlayer, not max_turn, game)[0]
            if alpbet < value:
                best_move = move
            value = min (value, alpbet)
            b = min ( b , value)
            if value <= a:
                break #( * a c u t o f f * )
        return value, best_move


if __name__ == "__main__":
    game = ConnectFour()
    depth = 10
    a = 10
    b = 10
    max_turn = True # true => max zaczyna
    # node, maximizingPlayer
    isEnded = False
    while not isEnded:
        game.state = game.state.make_move(alpha_beta(game.state, depth, a, b, "1", max_turn, game)[1])
        print(game.state)
        isEnded = game.state.is_finished()
    print("Game over! The winner is Player " + game.state.get_winner().char + "!")