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

int d = 1;

#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })


/* Player 2 is below 20, Player 1 is above 20 within the nmove */

int main(int argc, char *argv[])
{
    int i;
    phase = atoi(argv[1]);
    player = atoi(argv[2]);
    for (i = 3; i < 34; i++)
    {
        scanf("%d", &board[i - 3]);
    }

    for(i = -15; i < 16; i++)
    {
       if(i < -3)
          t0 += abs(i + 3) * abs(board[i + 15]);
       else
          t0 -= abs(i + 3) * abs(board[i + 15]);
       if(i < -1)
          t1 += abs(i + 1) * abs(board[i + 15]);
       else
          t1 -= abs(i + 1) * abs(board[i + 15]);
    }

    /* Phase 1 ! */
    
    for (i = 0; i < 31; i++)
    {
        if (board[i] > 0 && i != 12)
            p1w[board[i] - 1] = 1;   
        if (board[i] < 0)
            p2w[-1 * board[i] - 1] = 1; 
    }

    printf("%d\n", alpha_better());
    printf("%d\n", '-');

    return 0;
} /* end of main */ 

void torques(int *torque, char *moves)
{
   int i, tt0 = t0, tt1 = t1, len, pos, w;

   len = strlen(moves);
   for (i = 0; i < len + 1; i = i + 2)
   {
      pos = moves[i];
      if (moves[i + 1] < 20)
          w = moves[i + 1];
      else
          w = moves[i + 1] - 20;
      pos -= 15; /* Since board goes from 0 to 31, but positions go from -15 to 15 */
      if(pos < -3)
         tt0 += abs(pos + 3) * abs(w);
      else
         tt0 -= abs(pos + 3) * abs(w);
      if(pos < -1)
         tt1 += abs(pos + 1) * abs(w);
      else
         tt1 -= abs(i + 1) * abs(board[i + 15]);
   }
   torque[0] = tt0;
   torque[1] = tt1;
}

int play(char *moves)
{
   int tply = player;
   if ((strlen(moves)/4 % 2) == 1)
      if (player > 0)
         tply = player * -1;
      else
         tply = player;
   return(tply);
}


void apply_moves(char *moves, int *board_tmp)
{
    int len = strlen(moves), pos, i, w;
    for (i = 0; i < 32; i++)
    {
        board_tmp[i] = board[i];
    }
    for(i = 0; i < len + 1; i = i + 2)
    {
        pos = moves[i];
        printf("%d", pos); 
        w = (moves[i + 1] < 20) ? -1 * moves[i + 1] : moves[i + 1] - 20;
        board_tmp[pos] = w;
    }
}

/* Takes in a variables number of moves, realizes them in the board
 * calculates a score
 */
int eval_fn(char *moves)
{
    int score = 0, board_tmp[31];
    apply_moves(moves, board_tmp);
    /* calculate score */
    score = 7;
    return score;
}


int value(char *moves, int alpha, int beta, int depth, int max)
{
    int v = -inf, i, tp1w[7], tp2w[7], next, board_tmp[31], j, p;
    int t[2];
    char nmove[2];
    if (depth > d)
        return eval_fn(moves);
    for (i = 0; i < 7; i++)
    {
         tp1w[i] = p1w[i];
         tp2w[i] = p2w[i];
    }
    /* */
    for (i = 0; i < strlen(moves); i = i + 2)
    {
        if (moves[i + 1] < 20)
            tp2w[moves[i + 1]] = 0;
        else
            tp1w[moves[i + 1] - 20] = 0;
    }

    apply_moves(moves, board_tmp);

    p = play(moves);

    for (i = 0; i < 31; i++)
    {
        if(!board_tmp[i])
        {
            for(j = 0; j < 7; j++)
            {
               if(p > 0)
               {
                  if(tp1w[j])
                  {
                     nmove[0] = (char) i;
                     nmove[1] = (char) j + 1;
                  }
               }
               else
               {
                  if(tp2w[j])
                  {
                     nmove[0] = (char) i;
                     nmove[1] = (char) j + 21;       
                  }
               }
               torques(t, nmove);
               if(!(t[0] > 0 || t[1] < 0))
               {  
                  if (max)
                  {
                      next = 1;
                      v = max(v, value(strncat(moves, nmove, 2), 
                                           alpha, beta, depth + 1, 0));
                      if (v >= beta)
                          return v;
                      alpha = max(alpha, v);
                  }
                  else
                  {
                      next = 1;
                      v = min(v, value(strncat(moves, nmove, 2), 
                                           alpha, beta, depth + 1, 1));
                      if (v <= alpha)
                          return v;
                      beta = min(beta, v);
                  }
               }
            }
        }
    }
    if (!next)
        return player * play(moves) * inf * -1;
    return v;
}
                                 
/* Recrusively creates feasible sequences of nontipping moves and calls
 * the evaulation function
 */
int alpha_better()
{
    int best_v = inf, x;
    int i, j, p;
    int v = inf;
    int t[2];
    char nmove[2];
    char best_nmove[2];

    p = player;

    for (i = 0; i < 31; i++)
    {
        if(!board[i])
        {
            for(j = 0; j < 7; j++)
            {
               if(p > 0)
               {
                  if(p1w[j])
                  {
                     nmove[0] = (char) i;
                     nmove[1] = (char) j + 1;
                  }
               }
               else
               {
                  if(p2w[j])
                  {
                     nmove[0] = (char) i;
                     nmove[1] = (char) j + 21;       
                  }
               }
               torques(t, nmove);
               if(!(t[0] > 0 || t[1] < 0))
               {  
                  x = value(nmove, -1 * inf, inf, 0, 0);
                  if (x < best_v)
                  {
                      best_v = x;
                      best_nmove[0] = nmove[0];
                      best_nmove[1] = nmove[1];
                  }
               }
            }
        }
    }
    return best_v;
}



