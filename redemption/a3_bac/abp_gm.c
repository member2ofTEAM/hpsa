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

int d = 16;

int w1 = 4;
int w2 = 10;
int w3 = 2;
int w4 = 1;
int w5 = 2;
int w6 = 4;

int stable1[9] = {-12, -11, -10, -9, -8, -7, -6, -5, -4};
int stab23[5] = {-7, -6, -5, -4, -3}; /* 2 - 3 are the same */
int stab4[4] = {-5, -4, -3, -2};
int stab59[3] = {-4, -3, -2}; /* 5 - 9 are the same */
int stab1012[2] = {-3, -2}; /* 10-12 are the same */


#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })



/* Right now Phase 2 ignores the new rule! */

void alpha_better();

int main(int argc, char *argv[])
{
    int i, phase;

    player = atoi(argv[1]);
    pplayer = player;
    phase = atoi(argv[2]);
    
    for (i = 3; i < 34; i++)
    {
        board[i - 3] = atoi(argv[i]);
    }
    
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

    alpha_better(phase);

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
    int p1l = 0, p1r = 0;
    int num1 = 0, num2 = 0, count = 0;
    int nearmid = 0;
    int count_1 = 0, count_2 = 0;

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
          {
             if(i != 4)
                stab1++;
          }
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

    for(i = 0; i < 12; i++)
    {
       if(p1w[i] == 0)
          count_1++;
       else if(p2w[i] == 0)
          count_2++;
    }

    unstab1 = count_1 - stab1;
    unstab2 = count_2 - stab2;

    for(i = 0; i < 12; i++)
    {
       if(board[i] > 0)
       {
          p1l += board[i];
          if(i > 8)
             nearmid += board[i];
       }
    }
    for(i = 13; i < 31; i++)
    {
       if(board[i] > 0)
       {
          p1r += board[i];
          num1++;
          if(i < 15)
             nearmid += board[i];
       }
       else if(board[i] < 0)
          num2++;
    }

    if(abs(num1 - num2) > 2)
       count++;

//    if(pplayer == -1)
 //      score = w1 * stab2 - w2 * count;
 //   if(pplayer == 1)
 //      score = w3 * abs(t[0] * t[1]) - w4 * abs(p1l - p1r) - w5 * abs(t[0] - t[1]) + w6 * nearmid;

  // if(t[0] == 0 || t[1] == 0)
   //   return inf;
  // else
    //  return 500 - min(abs(t[0]),abs(t[1]));
//   if(t[0] == 0 || t[1] == 0)
  //    return inf;
//   else
//      return (1.0 / (float)(min(abs(t[0]),abs(t[1]))));
   
   //return 500 - min(abs(t[0]), abs(t[1]));
//    if(abs(t[0]) <= 4 || abs(t[1]) <= 4)
//    {
//       player = -1 * player;
//       return player * inf;
//    }

    if (exhausted)
    {
        player = -1 * player;
//        printf("%d\n", player * inf);
        return player * inf;
    }
    else
    {
//       printf("%d\n", 500 - min(abs(t[0]), abs(t[1])));
       return (500 - min(abs(t[0]), abs(t[1])));
    }
}

int value(int alpha, int beta, int depth, int max, int phase)
{
    int v = -inf, i, next = 0, j, *pw;
    int t[2], wleft = 0, tmp, p1wn = 0;
    

    for (i = 0; i < 12; i++)
    {
        wleft += p1w[i] + p2w[i];
    }
    if (!wleft)
    {
        phase += 1;
        p1w[0] = 2;
    }
	
    player = -1 * player;
	
    if (depth > d){
        return eval_fn(0, phase);
    }
    

    if (phase == 1)
    {
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
                    v = max(v, value(alpha, beta, depth + 1, 0, phase));
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
                    v = min(v, value(alpha, beta, depth + 1, 1, phase));
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
    }
    if (phase == 2)
    {
        for (i = 0; i < 31; i++)
        {
            if (board[i] > 0)
                p1wn += 1;
        }
        for (i = 0; i < 31; i++)
        {  
            if (p1wn > 0 && board[i] < 0)
                continue;
            if (!board[i])
                continue;
            tmp = board[i];
            board[i] = 0;
            torques(t);
            if(!tipped(t))
            {
                next = 1;
                if (max)
                {
                    v = max(v, value(alpha, beta, depth + 1, 0, phase)); 
                    if (v >= beta)
                    {
                        player = -1 * player;
                        board[i] = tmp;
                        return v;
                    }
                    alpha = max(alpha, v);
                }
                else
                {
                    v = min(v, value(alpha, beta, depth + 1, 1, phase));
                    if (v <= alpha)
                    {
                        player = -1 * player;
                        board[i] = tmp;
                        return v;
                    }
                    beta = min(beta, v);
                }
            }
            board[i] = tmp;
        }
    }
    if (!next)
        return eval_fn(1, phase);
    player = -1 * player;
    return v;
}
                                 
/* Recrusively realizes feasible sequences of nontipping moves and calls
 * the evaulation function
 */
void alpha_better(int phase)
{
    int best_v = -2 * inf, v = inf;
    int i, j;
    int t[2];
    int best_move[2];
    int *pw;
    int tmp;
    int p1wn = 0;
    

    if (phase == 1)
    {
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
                v = value((-1 * inf), inf, 1, 0, phase);
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
    }
    if (phase == 2)
    {
    for (i = 0; i < 31; i++)
    {
        if (board[i] > 0)
            p1wn += 1;
    }
    for (i = 0; i < 31; i++)
    {
        if (p1wn > 0 && board[i] < 0)
            continue;
        if (!board[i])
            continue;
        tmp = board[i];
        board[i] = 0;
        torques(t);
        if (!tipped(t))
        {
            v = value((-1 * inf), inf, 1, 0, phase);
            if (v > best_v)
            {
                best_v = v;
                best_move[0] = i;
                best_move[1] = tmp;
            }
        }
        board[i] = tmp;
    }
    }

    if (best_move[1] == 0)
    {
       if(phase == 1)
       {
          for(i = 0; i < 12; i++)
          {
             if(p1w[i] != 0 && player == 1)
             {
                best_move[1] = i + 1;
                break;
             }
             else if(p2w[i] != 0 && player == -1)
             {
                best_move[1] = i + 1;
                break;
             }
          }
          for(i = 0; i < 32; i++)
          {
             if(board[i] == 0)
             {
                best_move[0] = i;
                break;
             }
          }
       }
       else if(phase == 2)
       {
          for(i = 0; i < 32; i++)
          {
             if(board[i] > 0 && player == 1)
             {
                best_move[1] = board[i];
                best_move[0] = i;
                break;
             } 
          }
          if(best_move[1] == 0)
          {
             for(i = 0; i < 32; i++)
             {
                if(board[i] < 0)
                {
                   best_move[1] = board[i];
                   best_move[0] = i;
                   break;
                }
             }
          }
       }
    }
    printf("%d %d %d\n", best_move[0], abs(best_move[1]), best_v);
}




