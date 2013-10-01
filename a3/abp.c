#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
/*Change for Collin :) */
int phase;
int t0 = -9;
int t1 = -3;
int player;
int board[31];
int inf = 999999999;
int p1w[12];
int p2w[12];
int offset = 40;
int stable[88];
int w1 = 0;
int w2 = 0;
int w3 = 3;
int w4 = 10;
int w5 = 7;
int w6 = 15;
int d = 20;

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
    FILE *file;

    player = atoi(argv[1]);
    phase = atoi(argv[2]);
    
    for (i = 3; i < 34; i++)
    {
        board[i - 3] = atoi(argv[i]);
    }

    file = fopen("stable.dat", "r");
    assert(file);
   
    for(i = 0; i < 88; i++)
    {
       fscanf(file, "%d", &stable[i]);
    }
    fclose(file);
    
    //phase = 1;
    //player = 1;
    //board[11] = 3;
    
    for (i = 0; i < 12; i++)
    {
        p1w[i] = 1;
        p2w[i] = 1;
    }

    for (i = 0; i < 31; i++)
    {
        if (board[i] > 0 && i != 11)
            p1w[board[i] - 1] = 0;   
        if (board[i] < 0)
            p2w[(-1 * board[i]) - 1] = 0; 
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

/* tests torque without updating global torque. Use for scoring */
int ttorque(int weight, int pos, int *ttor, int *tor)
{
   int tt0, tt1;
   tor[0] = ttor[0];
   tor[1] = ttor[1];

   if(pos < -3)
      tor[0] += abs(pos + 3) * abs(board[pos + 15]);
   else
      tor[0] -= abs(pos + 3) * abs(board[pos + 15]);
   if(pos < -1)
      tor[1] += abs(pos + 1) * abs(board[pos + 15]);
   else
      tor[1] -= abs(pos + 1) * abs(board[pos + 15]);
}


int tipped(int *t)
{
    return (t[0] > 0 || t[1] < 0);
}

/* Calculates a score using the current state of the board
 */
int eval_fn(int exhausted)
{
    int score, i, j;
    int tor[2], ttor[2];
    int *pw;
    int numstab = 0; /* current number of stable blocks */
    int possible = 0;/* possible stable blockers */
    int possible2 = 0;
    int numopen = 0; /* number of open stable positions */
    int other = 0; /* moves on right side of board that aren't stable blockers */
    int numblock = 0;

    torques(ttor);
    score = 0;

    if(player > 0) 
       pw = p1w;
    else
       pw = p2w;

    /* checks for moves available that aren't stable */
    for(i = 0; i < 87; i = i + 2)
    {
       for(j = 0; j < 12; j++)
       {
          if(pw[j])
          { 
             if(j + 1 != stable[i])
             {
                ttorque(j + 1, stable[i + 1], ttor, tor);
                if(tor[0] <= 0 && tor[1] >= 0)
                {
                   possible++; /* possibly do some torque multiplication here */
                }
             }
          } 
       }
       if(possible)
       {
          possible2++;
          possible = 0;
       }
    }


    for(i = 0; i < 87; i = i + 2)
    {
       if(board[stable[i + 1] + 15] == stable[i])
          numstab++;
    }


    j = 0;
    for(i = 0; i < 87; i = i + 2)
    {
       if(board[stable[i + 1] + 15] != stable[i] && board[stable[i + 1] + 15] != 0 && j != stable[i + 1])
       {
          numblock++;
          j = stable[i + 1];
       }
    }

    /* other moves that aren't stable removing moves */
    for(i = -1; i < 16; i++)
    {
       for(j = 0; j < 12; j++)
       {
          if(p1w[j] != 0)
          {
             ttorque(j + 1, i, ttor, tor);
             if(tor[0] <= 0 && tor[1] >= 0)
                other++;  /* possibly some torque multiplication here */
          }
       }
    }

    for(i = 0; i < 15; i++)
    {
       if(board[i] == 0)
          numopen++;
    }

    score = w1 * possible2 + w2 * other + w3 * (-1 * ttor[0]) - w4 * numstab - w5*numopen + w6 * numblock;
   
    if (exhausted)
    {
        player = -1 * player;
        return score;
    }
    else
    {
        player = -1 * player;
        return score;
    }
}

int value(int alpha, int beta, int depth, int max)
{
    int v = -inf, i, next = 0, j, *pw;
    int t[2];

    player = -1 * player;

    if (depth > d){
        return eval_fn(0);
    }
    
    if (player > 0)
        pw = p1w;
    else
        pw = p2w;

    for (j = 0; j < 12; j++)
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
            if(!tipped(t))
            {
                next = 1;
                if (max)
                {
                    v = max(v, value(alpha, beta, depth + 1, 0));
                    if (v >= beta)
                    {
                        player = -1 * player;
                        board[i] = 0;
                        return v;
                    }
                    alpha = max(alpha, v);
                }
                else
                {
                    v = min(v, value(alpha, beta, depth + 1, 1));
                    if (v <= alpha)
                    {
                        player = -1 * player;
                        board[i] = 0;
                        return v;
                    }
                    beta = min(beta, v);
                }
            }
            board[i] = 0;
         }
         pw[j] = 1;
    }
    if (!next)
        return eval_fn(1);
    player = -1 * player;
    return v;
}
                                 
/* Recrusively realizes feasible sequences of nontipping moves and calls
 * the evaulation function
 */
void alpha_better()
{
    int best_v = -2 * inf, v = inf;
    int i, j;
    int t[2];
    int best_move[2];
    int *pw;

    if (player > 0)
        pw = p1w;
    else
        pw = p2w;

    for (j = 0; j < 12; j++)
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
            if(!tipped(t))
            {
                v = value((-1 * inf), inf, 1, 0);
                if (v > best_v)
                {
                    best_v = v;
                    best_move[0] = i;
                    best_move[1] = (player > 0) ? (j + 1) : (-1 * (j + 1));
                }
            }
            board[i] = 0;
        }
        pw[j] = 1;
    }
    printf("%d %d %d\n", best_move[0], abs(best_move[1]), best_v);

}




