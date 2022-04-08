# Tymon Kobylecki WSI 22L

from cmath import inf
import copy
import random
from two_player_games.player import Player
from two_player_games.move import Move
from two_player_games.state import State
from two_player_games.game import Game
from two_player_games.games.connect_four import ConnectFour, ConnectFourMove, ConnectFourState

def count_possible(node, move): # possible wins for max - possible wins for min
    col = print(move.column) # kolumna w ktorej postawiono ruch
    row = count_height(node.fields[col]) # wiersz w ktorym postawiono ruch
    for co in node.fields: # co - kolumna, point - pole
        for point in co:
            pass



def count_height(column): # do liczenia wysokosci pionka
    sum = 0
    for place in column:
        if place is not None:
            sum += 1
    return sum


def heuristic_val(node, maximizingPlayer, move = None):
    if node.get_winner() is not None:
        if node.get_winner().char == "1":
            return inf
        return -inf
    # count_possible(node, move)
    return 0

def is_terminal(node): #
    return node.is_finished()

def alpha_beta(board, depth , a , b , maximizingPlayer, max_turn, game, move=None): # Board jest typu ConnectFourState
    if depth == 0 or is_terminal(board):
        if depth == 0:
            return heuristic_val(board, maximizingPlayer, move), None
        return heuristic_val(board, maximizingPlayer), None
    moves = board.get_moves()
    best_moves = [None]
    if max_turn:
        value = -inf
        for move in moves:
            boardcopy = copy.deepcopy(board)
            boardcopy = boardcopy.make_move(move)
            alpbet = alpha_beta(boardcopy , depth-1 , a , b , maximizingPlayer, not max_turn, game, move)[0]
            if alpbet > value:
                best_moves = [move]
            elif alpbet == value:
                best_moves.append(move)
            value = max (value, alpbet)
            a = max(a, value)
            if value >= b:
                break #( * b c u t o f f * )
        return value, random.choice(best_moves)
    else:
        value = inf
        for move in moves:
            boardcopy = copy.deepcopy(board)
            boardcopy.make_move(move)
            alpbet = alpha_beta( boardcopy , depth-1 , a , b , maximizingPlayer, not max_turn, game, move)[0]
            if alpbet < value:
                best_moves = [move]
            elif alpbet == value:
                best_moves.append(move)
            value = min (value, alpbet)
            b = min ( b , value)
            if value <= a:
                break #( * a c u t o f f * )
        return value, random.choice(best_moves)

#startPlc
def generateHeuristics(n, m, k):
    board = makeBoard(7, 7)
    for i in range(7):
        for j in range(7):
            if i <= n - k:
                for kk in range(k):
                    board[i + kk][j] += 1
            if j <= m - k:
                for kk in range(k):
                    board[i][j + kk] += 1
            if i <= n - k and j <= m - k:
                for kk in range(k):
                    board[i + kk][j + kk] += 1
    for i in range(n-k+1):
        for j in range(k-1,m):
            for kk in range(k):
                board[i + kk][j - kk] += 1
    return board

# calculates value of heuristics function for given state of the game
def heuristicsFunction(board, k):
    heuristics = generateHeuristics(7, 7, k)
    sum = 0
    for i in range(7):
        for j in range(7):
            sum += heuristics[i][j] * board[i][j]
    winner = checkWinner(board, k)
    if winner == 1:
        sum += 5
    elif winner == -1:
        sum -= 5
    return sum
#stopPlc


if __name__ == "__main__":
    game = ConnectFour()
    depth = 10
    a = 10
    b = 10
    max_turn = True # true => max zaczyna
    # node, maximizingPlayer
    isEnded = False
    maximizingPlayer = Player("1")
    while not isEnded:
        try:
            game.state = game.state.make_move(alpha_beta(game.state, depth, a, b, maximizingPlayer, max_turn, game)[1])
            print(game.state)
            isEnded = game.state.is_finished()
        except AttributeError:
            print("It's a draw!")
            isEnded = True
    if game.state.get_winner() is not None:
        print("Game over! The winner is Player " + game.state.get_winner().char + "!")
