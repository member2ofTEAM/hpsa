#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

int board[33];

int main(int argc, char *argv[])
{
    int i;
    for (i = 1; i < 34; i++)
    {
        board[i - 1] = atoi(argv[i]);
    }

    

    return 0;
} /* end of main */ 


/* Takes in a variables number of moves, realizes them in the board
 * calculates a score
 */
int eval_fn(moves)
{

}

/* Recrusively creates feasible sequences of nontipping moves and calls
 * the evaulation function
 */
int alpha_better(d = 4)
{
    
    def max_value(game, alpha, beta, depth):
        if cutoff_test(game, depth):
            return eval_fn(game)
        v = -infinity
        for child in game[1].generate_children():
            v = max(v, min_value(child, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(game, alpha, beta, depth):
        if cutoff_test(game, depth):
            return eval_fn(game)
        v = infinity
        for child in game[1].generate_children():
            v = min(v, max_value(child, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = lambda game,depth: depth>d or \
                                      game[1].terminal_test()
    eval_fn = lambda game: game[1].get_utility()

    best_move = ((0, 0), infinity)
    for game in game.generate_children():
        x = min_value(game, -infinity, infinity, 0)
        if x < best_move[1]:
            best_move = (game[0], x)

    return best_move

}



