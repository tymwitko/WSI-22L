from cmath import inf

# def minimax( node , depth , maximizingPlayer ):
#     if depth == 0 or is_terminal(node):
#         return heuristic_val(node)
#     if player(node) == maximizingPlayer:
#         value = - inf
#         for child in node:
#             value = max( value, minimax (child , depth-1 , maximizingPlayer ) )
#         return value
#     else: # m i n i m i z i n g p l a y e r
#         vallue = inf
#         for child in node:
#             value = min ( value , minimax( child , depth-1 , maximizingPlayer ) )
#         return value

def heuristic_val(node):
    pass

def is_terminal(node): #
    move = ConnectFourMove(node)
    conforstate = ConnectFourState() # TODO: insert args
    conforstate.make_move(move)
    return ConnectFourState.is_finished()

def alpha_beta(node , depth , a , b , maximizingPlayer, max_turn ):
    if depth == 0 or is_terminal(node):
        return heuristic_val(node)
    if max_turn:
        value = -inf
        for child in node:
            value = max (value , alpha_beta( child , depth-1 , a , b , maximizingPlayer, not max_turn) )
            a = max(a , value)
            if value >= b:
                break #( * b c u t o f f * )
        return value
    else:
        value = inf
        for child in node:
            value = min (value, alpha_beta( child , depth - 1 , a , b , maximizingPlayer, not max_turn ) )
            b = min ( b , value)
            if value <= a:
                break #( * a c u t o f f * )
        return value