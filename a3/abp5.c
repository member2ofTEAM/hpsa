#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

//phase is not a global anymore
int t0 = -9;
int t1 = -3;
int player;
int pplayer;
int board[31];
int inf = 999999999;
int p1w[12];
int p2w[12];
int w1 = 1;
int w2 = 2;

int stable1[9] = {-12, -11, -10, -9, -8, -7, -6, -5, -4};
int stab23[5] = {-7, -6, -5, -4, -3}; /* 2 - 3 are the same */
int stab4[4] = {-5, -4, -3, -2};
int stab59[3] = {-4, -3, -2}; /* 5 - 9 are the same */
int stab1012[2] = {-3, -2}; /* 10-12 are the same */



/* Right now Phase 2 ignores the new rule! */

void alpha_better();

int main(int argc, char *argv[])
{
    int i, phase;
    int score;

    player = atoi(argv[1]);
    phase = atoi(argv[2]);
    pplayer = player;
    
    for (i = 3; i < 34; i++)
    {
        board[i - 3] = atoi(argv[i]);
    }
    
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

    score = eval_fn(1, phase);

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

int tipped(int *t)
{
    return (t[0] > 0 || t[1] < 0);
}

/* Calculates a score using the current state of the board
 */
int eval_fn(int exhausted, int phase)
{
    int score, t[2];
    int i, j, stab1 = 0, stab2 = 0, unstab1 = 0, unstab2 = 0;

    torques(t);

    /* counts stable configuations still on board */
    for(i = 0; i < 9; i++)
    {
       if(board[stable1[i] + 15] == 1)  
          stab1++;
       else if(board[stable1[i] + 15] == -1)
          stab2++; 
       if(i < 5)
       {
          if(board[stab23[i] + 15] == 2) /* weight 2 */
             stab1++;
          else if(board[stab23[i] + 15] == -2)
             stab2++;
          if(board[stab23[i] + 15] == 3)
             stab1++;
          else if(board[stab23[i] + 15] == -3)
             stab2++;
       }
       if(i < 4)
       {
          if(board[stab4[i] + 15] == 4)
             stab1++;
          else if(board[stab4[i] + 15] == -4)
             stab2++;
       }
       if(i < 3)
       {
          if(board[stab59[i] + 15] == 5)
             stab1++;
          else if(board[stab59[i] + 15] == -5)
             stab2++;
          if(board[stab59[i] + 15] == 6)
             stab1++;
          else if(board[stab59[i] + 15] == -6)
             stab2++;
          if(board[stab59[i] + 15] == 7)
             stab1++;
          else if(board[stab59[i] + 15] == -7)
             stab2++;
          if(board[stab59[i] + 15] == 8)
             stab1++;
          else if(board[stab59[i] + 15] == -8)
             stab2++;
          if(board[stab59[i] + 15] == 9)
             stab1++;
          else if(board[stab59[i] + 15] == -9)
             stab2++;
       }
       if(i < 2)
       {
          if(board[stab1012[i] + 15] == 10)
             stab1++;
          else if(board[stab1012[i] + 15] == -10)
             stab2++;
          if(board[stab1012[i] + 15] == 11)
             stab1++;
          else if(board[stab1012[i] + 15] == -11)
             stab2++;
          if(board[stab1012[i] + 15] == 12)
             stab1++;
          else if(board[stab1012[i] + 15] == -12)
             stab2++;
       }
    }


    /* counts unstable  */
    for(i = 3; i < 13; i++)
    {
       if(i == 3)
       {
          if(abs(board[i]) != 1 && board[i] > 0)
             unstab1++;
          else if (abs(board[i]) != 1 && board[i] < 0)
             unstab2++;
       }
       else if(i == 4)
       {
          if(abs(board[i]) != 1 && board[i] > 0)
             unstab1++;
          else if(abs(board[i]) != 1 && board[i] < 0)
             unstab2++;
       }
       else if(i == 5)
       {
          if(abs(board[i]) != 1 && board[i] > 0)
             unstab1++;
          else if(abs(board[i]) != 1 && board[i] < 0)
             unstab2++;
       }
       else if(i == 6)
       {
          if(abs(board[i]) != 1 && board[i] > 0)
             unstab1++;
          else if(abs(board[i]) != 1 && board[i] < 0)
             unstab2++;
       }
       else if(i == 7)
       {
          if(abs(board[i]) != 1 && board[i] > 0)
             unstab1++;
          else if(abs(board[i]) != 1 && board[i] < 0)
             unstab2++;
       }
       else if(i == 8)
       {
          if(abs(board[i]) != 1 && abs(board[i]) != 2 && board[i] > 0)
             unstab1++;
          else if(abs(board[i]) != 1 && abs(board[i]) != 2 && board[i] < 0)
             unstab2++;
       }
       else if(i == 9)
       {
          if(abs(board[i]) != 1 && abs(board[i]) != 2 && abs(board[i]) != 3 && board[i] > 0)
             unstab1++;
          else if(abs(board[i]) != 1 && abs(board[i]) != 2 && abs(board[i]) != 3 && board[i] < 0)
             unstab2++;
       }
       else if(i == 10)
       {
          if(abs(board[i]) != 1 && abs(board[i]) != 2 && abs(board[i]) != 3 && board[i] > 0)
          {
             if(abs(board[i]) != 4)
                unstab1++;
          }
          else if(abs(board[i]) != 1 && abs(board[i]) != 2 && abs(board[i]) != 3 && board[i] < 0)
          {
             if(abs(board[i]) != 4)
                unstab2++;
          }
       }
       else if(i == 11)
       {
          if(abs(board[i]) != 1 && abs(board[i]) != 2 && abs(board[i]) != 3 && board[i] > 0)
          {
             if(abs(board[i]) != 4 && abs(board[i]) !=5 && abs(board[i]) != 6)
             {
                if(abs(board[i]) != 7 && abs(board[i]) != 8 && abs(board[i]) != 9)
                   unstab1++;  
             }
          }
          else if(abs(board[i]) != 1 && abs(board[i]) != 2 && abs(board[i]) != 3 && board[i] < 0)
          {
             if(abs(board[i]) != 4 && abs(board[i]) !=5 && abs(board[i]) != 6)
             {
                if(abs(board[i]) != 7 && abs(board[i]) != 8 && abs(board[i]) != 9)
                   unstab2++;  
             }
          }
       }
       else if(i == 12)
       {
          if(abs(board[i]) != 2 && abs(board[i]) != 3 && abs(board[i]) != 4 && board[i] > 0)
          {
             if(abs(board[i]) != 5 && abs(board[i]) != 6 && abs(board[i]) != 7)
             {
                if(abs(board[i]) != 8 && abs(board[i]) != 9 && abs(board[i]) != 10)
                {
                   if(abs(board[i]) != 11 && abs(board[i]) != 12)
                      unstab1++;  
                }
             }
          }
          else if(abs(board[i]) != 2 && abs(board[i]) != 3 && abs(board[i]) != 4 && board[i] < 0)
          {
             if(abs(board[i]) != 5 && abs(board[i]) != 6 && abs(board[i]) != 7)
             {
                if(abs(board[i]) != 8 && abs(board[i]) != 9 && abs(board[i]) != 10)
                {
                   if(abs(board[i]) != 11 & abs(board[i]) != 12)
                      unstab2++;
                }
             }
          }
       }
       if(i == 13)
       {
          if(abs(board[i]) != 3 && abs(board[i]) != 4 && abs(board[i]) != 5 && board[i] > 0)
          {
             if(abs(board[i]) != 6 && abs(board[i]) != 7 && abs(board[i]) != 8)
             {
                if(abs(board[i]) != 9 && abs(board[i]) != 10 && abs(board[i]) != 11)
                {
                   if(abs(board[i]) != 12)
                      unstab1++;  
                }
             }
          }
          else if(abs(board[i]) != 3 && abs(board[i]) != 4 && abs(board[i]) != 5 && board[i] < 0)
          {
             if(abs(board[i]) != 6 && abs(board[i]) != 7 && abs(board[i]) != 8)
             {
                if(abs(board[i]) != 9 && abs(board[i]) != 10 && abs(board[i]) != 11)
                {
                   if(abs(board[i]) != 12)
                      unstab2++;
                }
             }
          }
       }
    }

    printf("stab1 = %d, stab2 = %d, unstab1 = %d, unstab2 = %d\n", stab1, stab2, unstab1, unstab2);

    if(pplayer == -1)
       score = w1 * stab2;
    if(pplayer == 1)
       score = w3 * abs(t[0] * t[1]) -  abs(t[0] - t[2]));


    if (exhausted)
    {
        player = -1 * player;
        return player * inf;
    }
    else
    {
        player = -1 * player;
        return score;
    }
}

