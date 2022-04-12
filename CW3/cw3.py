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
    col = move.column # kolumna w ktorej postawiono ruch
    row = count_height(node.fields[col]) # wiersz w ktorym postawiono ruch
    suma = 0
    suma += count_horizontal(node, col, row)
    suma += count_vertical(node, col, row)
    suma += count_diagonal(node, col, row)
    return suma

def count_horizontal(node, col, row):
    left = 0
    right = 0
    curr = node.fields[col][row]
    for i in range(3):
        i+=1
        try:
            if (node.fields[col-i][row] == None or node.fields[col-i][row] == curr) and col-i >= 0:
                left += 1
            else:
                break
        except IndexError:
            break
    for i in range(3):
        i+=1
        try:
            if node.fields[col+i][row] == None or node.fields[col+i][row] == curr:
                right += 1
            else:
                break
        except IndexError:
            break
    if left+right < 3:
        return 0
    return left+right-2

def count_vertical(node, col, row):
    top = len(node.fields[col]) - row
    if top > 3:
        top = 3
    bottom = 0
    for i in range(row):
        try:
            if node.fields[col][row-i-1] != node.fields[col][row]:
                break
            bottom += 1
        except IndexError:
            break
    if top + bottom < 3:
        return 0
    return top + bottom - 2

def count_diagonal(node, col, row):
    # print(node)
    sumka = 0
    #\
    left = 0
    right = 0
    curr = node.fields[col][row]
    for i in range(3):
        i+=1
        try:
            if (node.fields[col-i][row+i] == None or node.fields[col-i][row+i] == curr) and col-i >= 0:
                left += 1
            else:
                break
        except IndexError:
            break
    for i in range(3):
        i+=1
        try:
            if (node.fields[col+i][row-i] == None or node.fields[col+i][row-i] == curr) and row-i >= 0:
                right += 1
            else:
                break
        except IndexError:
            break
    if left+right < 3:
        sumka += 0
    else:
        sumka += left + right - 2
    
    # /
    left = 0
    right = 0
    curr = node.fields[col][row]
    for i in range(3):
        i+=1
        try:
            if (node.fields[col-i][row-i] == None or node.fields[col-i][row-i] == curr) and col-i >= 0 and row-i >= 0:
                left += 1
            else:
                break
        except IndexError:
            break
    for i in range(3):
        i+=1
        try:
            if (node.fields[col+i][row+i] == None or node.fields[col+i][row+i] == curr):
                right += 1
            else:
                break
        except IndexError:
            break
    if left+right < 3:
        sumka += 0
    else:
        sumka += left + right - 2

    return sumka

def count_height(column): # do liczenia wysokosci pionka - UWAGA - liczone od 0
    suma = 0
    for place in column:
        if place is not None:
            suma += 1
    return suma - 1


def heuristic_val(node, maximizingPlayer, move, max_turn):
    # print("PROBUJE")
    # print(node)
    if node.get_winner() is not None:
        if node.get_winner().char == "1":
            # print("pog, wygram ja, max")
            return 5000
        # print("pog, wygram ja, jarzabek")
        return -5000
    # count_possible(node, move)
    if max_turn:
        return count_possible(node, move)
    else:
        return -count_possible(node, move)

def is_terminal(node): #
    return node.is_finished()

def alpha_beta(board, depth , a , b , maximizingPlayer, max_turn, game, move=None): # Board jest typu ConnectFourState
    if depth == 0 or is_terminal(board):
        if depth == 0:
            return heuristic_val(board, maximizingPlayer, move, not max_turn), None # not max_turn żeby nie zmieniało nam tury na liściach
        return heuristic_val(board, maximizingPlayer, move, not max_turn), None
    moves = board.get_moves()
    best_moves = [None]
    if max_turn:
        value = -inf
        for move in moves:
            boardcopy = copy.deepcopy(board)
            boardcopy = boardcopy.make_move(move)
            alpbet = alpha_beta(boardcopy , depth-1 , a , b , maximizingPlayer, not max_turn, game, move)[0]
            # print("niby turn maxima", alpbet)
            if alpbet > value:
                best_moves = [move]
                # print(move.column, depth)
                # print("alpbet > value")
                # print(alpbet, value)
            elif alpbet == value:
                best_moves.append(move)
            value = max (value, alpbet)
            # a = max(a, value)
            if value >= b:
                break #( * b c u t o f f * )
        return value, random.choice(best_moves)
    else:
        value = inf
        for move in moves:
            boardcopy = copy.deepcopy(board)
            boardcopy = boardcopy.make_move(move)
            alpbet = alpha_beta( boardcopy , depth-1 , a , b , maximizingPlayer, not max_turn, game, move)[0]
            # print("niby turn minima", alpbet)
            if alpbet < value:
                best_moves = [move]
                # print(move.column)
                # print("alpbet < value")
                # print(alpbet, value)
            elif alpbet == value:
                best_moves.append(move)
            value = min (value, alpbet)
            # b = min ( b , value)
            if value <= a:
                break #( * a c u t o f f * )
        return value, random.choice(best_moves)


if __name__ == "__main__":
    game = ConnectFour()
    depth = 3
    a = -5001
    b = 5001
    max_turn = True # true => max zaczyna
    # node, maximizingPlayer
    isEnded = False
    maximizingPlayer = Player("1")
    while not isEnded:
        try:
            move = alpha_beta(game.state, depth, a, b, maximizingPlayer, max_turn, game)[1]

            # moves = game.state.get_moves()
            # for movie in moves:
            #     cop = copy.deepcopy(game)
            #     cop.state = cop.state.make_move(movie)
            #     print(cop.state)
            #     print("Heurystyka: poziomo: " + str(count_horizontal(cop.state, movie.column, count_height(cop.state.fields[movie.column]))) + " + pionowo: " + str(count_vertical(cop.state, movie.column, count_height(cop.state.fields[movie.column]))) + " + ukosnie: " + str(count_diagonal(cop.state, movie.column, count_height(cop.state.fields[movie.column]))) + " = " + str(heuristic_val(cop.state, maximizingPlayer, movie, max_turn)))
            

            game.state = game.state.make_move(move)
            print("-----------\nUWAGA NOWY RUCH\n-------------")
            print(game.state)
            print("Heurystyka: poziomo: " + str(count_horizontal(game.state, move.column, count_height(game.state.fields[move.column]))) + " + pionowo: " + str(count_vertical(game.state, move.column, count_height(game.state.fields[move.column]))) + " + ukosnie: " + str(count_diagonal(game.state, move.column, count_height(game.state.fields[move.column]))) + " = " + str(heuristic_val(game.state, maximizingPlayer, move, max_turn)))
            max_turn = not max_turn
            # isEnded = True
            isEnded = game.state.is_finished()
        except AttributeError:
            print("It's a draw!")
            isEnded = True
    if game.state.get_winner() is not None:
        print("Game over! The winner is Player " + game.state.get_winner().char + "!")
