#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

int phase;
int t0 = -9;
int t1 = -3;
int player;
int board[31];
int inf = 999999999;
int p1w[7];
int p2w[7];
int offset = 40;

int d = 8;

#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })


/* Player 2 is below 20, Player 1 is above 20 within the nmove */

void alpha_better();

int main(int argc, char *argv[])
{
    int i;
    phase = 1;
    player = 1;

    board[12] = 3;
    
    /* Phase 1 ! */
    
    for (i = 0; i < 7; i++)
    {
        p1w[i] = 1;
        p2w[i] = 1;
    }

    for (i = 0; i < 31; i++)
    {
        if (board[i] > 0 && i != 12)
            p1w[board[i] - 1] = 0;   
        if (board[i] < 0)
            p2w[-1 * board[i] - 1] = 0; 
    }

    alpha_better();

    return 0;
} /* end of main */ 

void torques(int *torque)
{
   int i, tt0 = -9, tt1 = -3;
 
   for(i = -15; i < 16; i++)
   {
       if(i < -3)
          tt0 += abs(i + 3) * abs(board[i + 15]);
       else
          tt0 -= abs(i + 3) * abs(board[i + 15]);
       if(i < -1)
          tt1 += abs(i + 1) * abs(board[i + 15]);
       else
          tt1 -= abs(i + 1) * abs(board[i + 15]);
   }

   torque[0] = tt0;
   torque[1] = tt1;
}

/* Calculates a score using the current state of the board
 */
int eval_fn()
{
    int score;
    /* calculate score */
    score = 7;
    return score;
}


int value(int alpha, int beta, int depth, int max)
{
    int v = -inf, i, next = 0, j, p, *pw;
    int t[2];
    char nmove[3];
    if (depth > d)
        return eval_fn();
    
    player = -1 * player;
    if (player > 0)
        pw = p1w;
    else
        pw = p2w;

    for (j = 0; j < 7; j++)
    {
        if (pw[j])
            pw[j] = 0;
        else
            continue;
        for (i = 0; i < 31; i++)
        {
            if (board[i])
                continue;
            board[i] = player * (j + 1);
            torques(t);
            if(!(t[0] > 0 || t[1] < 0))
            {
                next = 1;
                if (max)
                {
                    v = max(v, value(alpha, beta, depth + 1, 0));
                    if (v >= beta)
                        return v;
                    alpha = max(alpha, v);
                }
                else
                {
                    v = min(v, value(alpha, beta, depth + 1, 1));
                    if (v <= alpha)
                        return v;
                    beta = min(beta, v);
                }
            }
            board[i] = 0;
         }
         pw[j] = 1;
    }
    player = -1 * player;
    if (!next)
        return player * inf * -1;
    return v;
}
                                 
/* Recrusively realizes feasible sequences of nontipping moves and calls
 * the evaulation function
 */
void alpha_better()
{
    int best_v = -1 * inf, x;
    int i, j;
    int v = inf;
    int t[2];
    int best_move[2];
    int *pw;

    if (player > 0)
        pw = p1w;
    else
        pw = p2w;

    for (j = 0; j < 7; j++)
    {
        if(pw[j])
            pw[j] = 0;
        else
            continue;
        for (i = 0; i < 31; i++)
        {
            if (board[i])
                continue;
            board[i] = player * (j + 1);
            torques(t);
            if(!(t[0] > 0 || t[1] < 0))
            {
                x = value(-1 * inf, inf, 1, 0);
                if (x > best_v)
                {
                    best_v = x;
                    best_move[0] = i;
                    best_move[1] = (player > 0) ? j + 1 : -1 * (j + 1);
                }
            }
            board[i] = 0;
        }
        pw[j] = 1;
    }
    printf("%d %d %d\n", best_move[0], best_move[1], best_v);

}




