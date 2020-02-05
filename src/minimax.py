
""" Generic minimax function. Calls on static eval for the heuristic, also has 
optional parameter max_depth to allow us to control the performance"""

def minimax(game, alpha, beta, depth, max_depth = 3):
    if depth == max_depth:
        return game.static_eval(), None
    elif game.player == 'O':
        best = None
        for state in game.gen_successors():
            bv, player_move = minimax(state, alpha, beta, depth + 1)
            if bv > alpha:
                alpha = bv
                best = state.last_move
            if alpha >= beta:
                return beta, best
        return alpha, best
    else:
        best = None
        for state in game.gen_successors():
            bv, comp_move = minimax(state, alpha, beta, depth +1)
            if bv < beta:
                beta = bv
                best = state.last_move
            if beta <= alpha:
                return alpha, best
            
        return beta, best
    