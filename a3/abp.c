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
int inf = 999999999999999;
int p1w[7];
int p2w[7];

int d = 4;

int main(int argc, char *argv[])
{
    int i;
    phase = argv[1];
    player = argv[2];
    for (i = 3; i < 34; i++)
    {
        board[i - 3] = atoi(argv[i]);
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
    
    for (i = 0; i < 31; i++)
    {
        if (board[i] > 0)
            p1w[board[i]] = 1;
        else if (board[i] < 0)
            p2w[-1 * board[i]] = 1;
    }

    return 0;
} /* end of main */ 

void torques(int *torque, moves)
{
   int i, tt0 = t0, tt1 = t1, len, pos, w;

   len = strlen(moves);
   for (i = 0; i < len + 1; i = i + 4)
   {
      pos = atoi(moves[i])*10 + atoi(moves[i + 1]);
      w = atoi(moves[i + 2]) < 0 : -1* atoi(moves[i + 3]) : atoi(moves[i + 3]);
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

   return(0);
}

int play(moves)
{
   int tply = player;
   if (strlen(moves)/4 % 2) == 1
      tply = player > 0 : player * -1 : player;
   return(tply);
}


void apply_moves(moves, *board_tmp)
{
    int len = strlen(moves), pos, i;
    for (i = 0; i < 32; i++)
    {
        board_tmp[i] = board[i];
    }
    for (i = 0; i < len + 1; i = i + 4)
    {
        pos = atoi(moves[i])*10 + atoi(moves[i + 1]);
        w = moves[i + 2] == '-' : -1* atoi(moves[i + 3]) : atoi(moves[i + 3]);
        board_tmp[pos] = w;
    }
   return 0;
}

/* Takes in a variables number of moves, realizes them in the board
 * calculates a score
 */
int eval_fn(moves)
{
    int score = 0, board_tmp[31];
    int board_tmp = apply_moves(moves, board_tmp);
    /* calculate score */
    score = 7;
    return score;
}


int max_value(char *moves, int alpha, int beta, int depth)
{
    int v = -inf, i, tp1w[7], tp2w[7], next, board_tmp[31], j, p;
    int t[2];
    char nmove[4];
    if (depth > d)
        return eval_fn(moves);
    for (i = 0; i < 7; i++)
    {
         tp1w[i] = p1w[i];
         tp2w[i] = p2w[i];
    }
    /* */
    for (i = 0; i < strlen(moves); i = i + 4)
    {
        if (moves[i + 2] == '-')
            tp2w[atoi(moves[i + 3])] = 0;
        else
            tp1w[atoi(moves[i + 3])] = 0;
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
                     nmove[0] = (char) i / 10 + 48;
                     nmove[1] = (char) i % 10 + 48;
                     nmove[2] = (char) 48;
                     nmove[3] = (char) j + 48;
                  }
               }
               else
               {
                  if(tp2w[j])
                  {
                     nmove[0] = (char) i / 10 + 48;
                     nmove[1] = (char) i % 10 + 48;
                     nmove[2] = '-';
                     nmove[3] = (char) j + 48;       
                  }
               }
               torques(t, nmove);
               if(!(t[0] > 0 || t[1] < 0))
               {  
                  next = 1;
                  v = max(v, min_value(strcat(moves, nmove), 
                                       alpha, beta, depth + 1));
                  if (v >= beta)
                      return v;
                  alpha = max(alpha, v);
               }
            }
        }
    }
    if (!next)
        return player * play(moves) * inf * -1;
    return v;
}

int min_value(char *moves, int alpha, int beta, int depth)
{
    int i, tp1w[7], tp2w[7], next, board_tmp[31], j, p;
    int v = inf;
    int t[2];
    char nmove[4];
    if (depth > d)
        return eval_fn(moves);
    for (i = 0; i < 7; i++)
    {
         tp1w[i] = p1w[i];
         tp2w[i] = p2w[i];
    }
    /* */
    for (i = 0; i < strlen(moves); i = i + 4)
    {
        if (moves[i + 2] == '-')
            tp2w[atoi(moves[i + 3])] = 0;
        else
            tp1w[atoi(moves[i + 3])] = 0;
    }

    apply_moves(moves, board_tmp);

    p = play(moves);

    for (i = 0; i < 31; i++)
    {
w
        if(!board_tmp[i])
        {
            for(j = 0; j < 7; j++)
            {
               if(p > 0)
               {
                  if(tp1w[j])
                  {
                     nmove[0] = (char) i / 10 + 48;
                     nmove[1] = (char) i % 10 + 48;
                     nmove[2] = (char) 48;
                     nmove[3] = (char) j + 48;
                  }
               }
               else
               {
                  if(tp2w[j])
                  {
                     nmove[0] = (char) i / 10 + 48;
                     nmove[1] = (char) i % 10 + 48;
                     nmove[2] = '-';
                     nmove[3] = (char) j + 48;       
                  }
               }
               torques(t, nmove);
               if(!(t[0] > 0 || t[1] < 0))
               {  
                  next = 1;
                  v = min(v, max_value(strcat(moves, nmove), 
                                       alpha, beta, depth + 1));
                  if (v <= alpha)
                      return v;
                  beta = min(beta, v);
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
    char nmove[4];

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
                     nmove[0] = (char) i / 10 + 48;
                     nmove[1] = (char) i % 10 + 48;
                     nmove[2] = (char) 48;
                     nmove[3] = (char) j + 48;
                  }
               }
               else
               {
                  if(p2w[j])
                  {
                     nmove[0] = (char) i / 10 + 48;
                     nmove[1] = (char) i % 10 + 48;
                     nmove[2] = '-';
                     nmove[3] = (char) j + 48;       
                  }
               }
               torques(t, nmove);
               if(!(t[0] > 0 || t[1] < 0))
               {  
                  x = min_value(nmove, -1 * inf, inf, 0)
                  if (x < best_v)
                  {
                      best_v = x
                      best_nmove[0] = nmove[0];
                      best_nmove[1] = nmove[1];
                      best_nmove[2] = nmove[2];
                      best_nmove[3] = nmove[3];
                  }
               }
            }
        }
    }
    if (!next)
        return player * play(moves) * inf * -1;

    return best_v
}



