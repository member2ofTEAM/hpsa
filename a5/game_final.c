#include <stdio.h>
#include "tinymt32.h"
#include <stdlib.h>
#include <math.h>
#include <sys/types.h>
#include <unistd.h>
#include <inttypes.h>
#include "tinymt32.c"
#include <time.h>
#include <assert.h>

void test_algorithm();
int do_move_random(int *move);
int do_move_algorithm(int *move);
int do_move_manual(int *move);
void print_board();
void decent_random(int *move);
void alpha_better(int *move, int algo, int max_depth);
int value(int alpha, int beta, int depth, int max, int algo, int max_depth);
int eval_fn();
int our_area();
void update_point(int *pos, int do_flag, int *move);
double exact_pull(int *pos);
int next_point(int *move, int which, int algo);
int get_random_int();


#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
          __typeof__ (b) _b = (b); \
               _a > _b ? _a : _b; })

#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
          __typeof__ (b) _b = (b); \
               _a < _b ? _a : _b; })


const int BOARD_SIZE = 1000;
const double INF = 10000000;
double board[1000][1000];
int NUM_MOVES_REMAINING = 30;
int MAX_NUMBER_OF_MOVES = 30;
int moves[60];
int MAX_NUMBER_OF_POINTS = 1000000;
int next_to_set;
//Player 1 gets to start
int player_to_start = 0;
tinymt32_t state;

//char INPUT_FILENAME[8];

/*
 *
 * CHANGING THE BOARD
 * PLayer 0 has -INf and negative pull, Player 1 has +INF and positive pull
 */                                                                 
                                                                    
void init_board()                                                   
{                                                                   
    int pos[2], i = 0;
    FILE *file;                                                     
    file = fopen("input", "r");
    assert(file);                                                   
                                                                    
    //TODO NEED TO FLIP NEXT_TO_SET AS MANY TIMES AS THERE ARE MOVES!
    for (i = 0; i < MAX_NUMBER_OF_POINTS; i++)
    {
        if (!next_point(pos, i, 1))
            break;
        if(abs(board[pos[0]][pos[1]]) != INF)
            board[pos[0]][pos[1]] = exact_pull(pos);
    }

    fclose(file);
}

double distance_squared(int x0, int y0, int x1, int y1)
{
    return (x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1);
}

void update_point(int *pos, int do_flag, int *move)
{
    int i = pos[0], j = pos[1];
    double d = 0.0;
    //Ignore pixels with stones set
    if (abs(board[i][j]) != INF)
    {
        d = distance_squared(move[0], move[1], i, j);
        if(d)
        {
            if (!do_flag)
                d = -d;
            board[i][j] += (1.0 / d);
        }
    }
}

double exact_pull(int *pos)
{
    int i = 0;
    double d = 0.0, pull = 0.0;
    for (i = 0; i < MAX_NUMBER_OF_MOVES - NUM_MOVES_REMAINING; i++)
    {
        d = distance_squared(pos[0], pos[1], moves[i * 2], moves[i * 2 + 1]);
        if(d)
	{
            if (i % 2)
	        pull += (1.0 / d);
	    else
	        pull -= (1.0 / d);
	}
    }
    return pull;
}

int execute_move(int *move, int do_flag, int algo)
{
    int next[2], i;
    
    //Make sure the move is valid
    if (move[0] < 0 || move[0] > 999 || move[1] < 0 || move[1] > 999)
        return -1;

    if (do_flag)
    {
        //Make sure stone can be placed
        if (abs(board[move[0]][move[1]]) == INF)
            return -1;
        //Place the stone
        if (next_to_set)
            board[move[0]][move[1]] = INF;
        else
            board[move[0]][move[1]] = -INF;
    }
    else
    {
        //Make sure stone can be removed
        if (abs(board[move[0]][move[1]]) != INF)
            return -1;
        //Restore its value
        board[move[0]][move[1]] = exact_pull(move); //is this necessary?
    }

    //Update the board
    for(i = 0; i < MAX_NUMBER_OF_POINTS; i++)
    {
        if (!next_point(next, i, 1))
            break;
        //If we are not next_to_set subtract the pull
        update_point(next, next_to_set, move);
    }

    //Flip the player
    next_to_set = next_to_set > 0 ? 0 : 1;


    //Store the move, and adjust number of moves remaining
    i = MAX_NUMBER_OF_MOVES - NUM_MOVES_REMAINING;
    if (do_flag)
    {
        moves[i * 2]       = move[0];
        moves[(i * 2) + 1] = move[1];
        NUM_MOVES_REMAINING--;
    }
    else
    {
        i = i - 1;
        moves[i * 2]       = -1;
        moves[(i * 2) + 1] = -1;
        NUM_MOVES_REMAINING++;
    }

    return our_area();
}
//move is in the format [x, y] as a 2 dim array
//returns the area owned by us
int do_move(int *move)
{
    return execute_move(move, 1, 1);
}

//move is in the format [x, y] as a 2 dim array
int undo_move(int *move)
{
    return execute_move(move, 0, 1);
}

int do_move_coarse(int *move, int algo)
{
    return execute_move(move, 1, algo);
}

int undo_move_coarse(int *move, int algo)
{
    return execute_move(move, 0, algo);
}

//Sees if opponent made a greedy move
int greedy_check(int *move, double range)
{
   int last, i;
   double distance;

   last = MAX_NUMBER_OF_MOVES - NUM_MOVES_REMAINING;
   if(last < 2)
      return 0;
   for(i = 0; i < last; i += 2)
   {
      if(!next_to_set)
      {  
         distance = distance_squared(move[i], move[i + 1], move[last - 2], move[last - 1]);
         distance = distance * distance;
         if(distance > range)
            return 1;
      }
      else
      {  
         distance = distance_squared(move[i + 2], move[i + 2 + 1], move[last - 2], move[last - 1]);
         distance = distance * distance;
         if(distance > range)
            return 1;
      }
   }
   return 0;
}

//Checks for other nearby stones given that it passes border check
int stone_check(int x, int y)
{
   if(abs(board[x][y]) == INF)
      return 0;
   return 1;
}

// Chooses the greedy location with the highest value
void highest_value_greedy(int *move, int x, int y)
{
   int i, j;
   double val, best_val = -1;

   for(i = -1; i <= 1; i++)
   {
      for(j = -1; j <= 1; j++)
      {
         if((x + i < 0) || (x + i >= BOARD_SIZE) || (y + i < 0) || (y + i >= BOARD_SIZE))
            continue;
         if(!stone_check(x + i, y + j))
            continue;
         val = board[x + i][y + j];
         if(val > best_val)
         {
            best_val = val;
            move[0] = x + i; 
            move[1] = y + j;
         }
      }
   }
}

void nearby_greedy(int *move, int x, int y)
{
   int i, j;
   double score, bestscore = -1;
   int best_move[2];

   for(i = -1; i <= 1; i++)
   {
      for(j = -1; j <= 1; j++)
      {
         if((x + i < 0) || (x + i >= BOARD_SIZE) || (y + i < 0) || (y + i >= BOARD_SIZE))
            continue;
         if(!stone_check(x + i, y + j))
            continue;
         move[0] = x + i; 
         move[1] = y + j;
         score = do_move(move);
         if(score > bestscore)
         {
            bestscore = score;
            best_move[0] = move[0];
            best_move[1] = move[1];
         }
         undo_move(move);
      }
   }
   move[0] = best_move[0];
   move[1] = best_move[1];
}


void lowest_value(int *move, int dist_from_border)
{
   int i, j;
   double lowest = 10000;
  
   for(i = dist_from_border; i < BOARD_SIZE - dist_from_border; i++)
   {
      for(j = dist_from_border; j < BOARD_SIZE - dist_from_border; j++)
      {
         if(abs(board[i][j]) < lowest)
         {
            lowest = board[i][j];
            move[0] = i;
            move[1] = j;
         }
      }
   }
}

void lowest_random(int *move, int dist_from_border, double threshold)
{
   int i, j, k, random;
   int possible[20000] = {-1};
   int found = 0;

   for(i = dist_from_border; i < BOARD_SIZE - dist_from_border; i++)
   {
      found = 0;
      for(j = dist_from_border; j < BOARD_SIZE - dist_from_border; j++)
      {
         if(abs(board[i][j]) < threshold)
         {
            possible[k] = i; 
            possible[k + 1] = j;
            k += 2;
            j += 24;
            found = 1;
            if(k >= 20000)
               break;
         }
      }
      if(found)
         i += 24;
   }
   random = get_random_int();
   random = random % k;
   while(possible[random] == -1)
   {
      random = get_random_int();
      random = random % k;
   }
   if(random % 2 == 1)
      random = random - 1;
   move[0] = possible[random];
   move[1] = possible[random + 1];
}

int next_point(int *move, int which, int algo)
{
    int MAX_POINTS;
    int x, y;

    if (algo == 1)
    {
        MAX_POINTS = 1000000;
        if (which >= MAX_POINTS)
            return 0;
        move[0] = which / 1000;
        move[1] = which % 1000;
        return 1;
    }
    if (algo == 2)
    {
        MAX_POINTS = 100;
        if (which >= MAX_POINTS)
            return 0;
        move[0] = (which / 10) * 100;
        move[1] = (which % 10) * 100;
        return 1;
    }
    if (algo == 3)
    {
        //DO SOMETHING WITH GAME BOARD
        //MAKE ARRAY OF POINTS
        MAX_POINTS = 40;
        if (which > MAX_POINTS)
            return 0;
        //SET MOVE TO which POINT
        return 1;
     }
     //Greedy next to their stones. Chooses the one 
     //with the highest value
     if (algo == 4)
     {
        move[0] = -1;
        move[1] = -1;
        MAX_POINTS = (MAX_NUMBER_OF_MOVES / 2);
        if (which >= MAX_POINTS)
           return 0;
        if(NUM_MOVES_REMAINING == MAX_NUMBER_OF_MOVES)
        {
           move[0] = 499;
           move[1] = 499;
           which = MAX_POINTS;
           return 1;
        }
       if(!next_to_set)
        {
           x = moves[(which * 2) - 2];
           y = moves[(which * 2) - 2 + 1];
           highest_value_greedy(move, x, y);
        }
        else
        {
           x = moves[which * 2];
           y = moves[which * 2 + 1];
           highest_value_greedy(move, x, y);
        } 
        if(move[0] == -1 && move[1] == -1)
        {
           move[0] = get_random_int();
           move[1] = get_random_int();
           return 0;
        }
        return 1;
     }
     // Greedy next to their stone. Choose the best one
     if(algo == 5)
     {
        move[0] = -1;
        move[1] = -1;
        MAX_POINTS = (MAX_NUMBER_OF_MOVES / 2);
        if (which >= MAX_POINTS)
           return 0;
        if(NUM_MOVES_REMAINING == MAX_NUMBER_OF_MOVES)
        {
           move[0] = 499;
           move[1] = 499;
           which = MAX_POINTS;
           return 1;
        }
        if(!next_to_set)
        { 
           x = moves[(which * 2) - 2];
           y = moves[(which * 2) - 2 + 1];
           nearby_greedy(move, x, y);
        }
        else
        {
           x = moves[which * 2];
           y = moves[which * 2 + 1];
           nearby_greedy(move, x, y);
        } 
        if(move[0] == -1 && move[1] == -1)
        {
           move[0] = get_random_int();
           move[1] = get_random_int();
           return 0;
        }
        return 1;
     }
     // Random algorithm
     if (algo == 6)
     {
        MAX_POINTS = 400;
        if(which > MAX_POINTS)
           return 0;
        move[0] = get_random_int();
        move[1] = get_random_int();
     }
     //lowest value on the board 
     if(algo == 7)
     {
        if(MAX_NUMBER_OF_MOVES == NUM_MOVES_REMAINING)
        {
           move[0] = 499;
           move[1] = 499;
           return 1;
        }
        MAX_POINTS = 1;
        if(which > MAX_POINTS)
           return 0;
        lowest_value(move, 50);
        return 1;
     }
     //lowest value from random values
     if(algo == 8)
     {
        if(MAX_NUMBER_OF_MOVES == NUM_MOVES_REMAINING)
        {
           move[0] = 499;
           move[1] = 499;
           return 1;
        }
        MAX_POINTS = 2;
        if(which > MAX_POINTS)
           return 0;
        lowest_random(move, 25, .00003);
        return 1;
     }     

     return 0;
}


/*
 *
 *
 *
 */

/*
 *
 * PERFORMING TEST / STATS
 *
 */

int our_area()
{
    int i, j, area = 0;
    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
           if (board[i][j] > 0)
               area++;
        }
    }
    return area;
}

void print_board()
{
    int i, j;
    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
            printf("%17.16lf ", board[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void save_stats(int score)
{
    FILE *stats;
    int i;
    stats = fopen("output.csv", "a+");
    assert(stats);
    fprintf(stats, "%d ", player_to_start);
    fprintf(stats, "%d", score);
    for(i = 0; i < MAX_NUMBER_OF_MOVES; i++)
    {
       fprintf(stats, ", %d %d", moves[i * 2], moves[(i * 2) + 1]);
    }
    fprintf(stats, "\n");
    
}

void test_algorithm()
{
    int score, move[2];
    while(NUM_MOVES_REMAINING)
    {
        score = do_move_manual(move);
        score = do_move_algorithm(move);
        printf("%d %d\n", move[0], move[1]);

    }
    printf("%d", our_area());
    //print_board();
    if(score <= 500000)
       save_stats(score);
}

/*
 *
 *
 *
 */

int main(int argc, char *argv[])
{
    //TODO: READ IN NAME OF INPUT FILE
//    int i;
//    for (i = 1; i < argc; i++)
//        INPUT_FILENAME[i] = argv[i];
//    init_board();
    int move[2], i;
    int algo_0 = 5;
    int algo_1 = 4;
    uint32_t seed = getpid();
    tinymt32_init(&state, seed);
    for(i = 0; i < 60; i++)                                         
       moves[i] = -1;
    i = 0;
    while(2 * i < argc - 1)
    { 
       moves[i * 2] = atoi(argv[i * 2 + 1]);
       moves[i * 2 + 1] = atoi(argv[i * 2 + 1 + 1]);
       if(i % 2)
          board[moves[i * 2]][moves[i * 2 + 1]] = INF;
       else
          board[moves[i * 2]][moves[i * 2 + 1]] = -INF;
       i++;
       NUM_MOVES_REMAINING--;
       next_to_set = next_to_set > 0 ? 0 : 1;
    }
    init_board();
    if(NUM_MOVES_REMAINING > 5)
       algo_1 == 4;
    else
       algo_1 == 5;
    if (next_to_set)
        alpha_better(move, algo_0, 0); 
    else
        alpha_better(move, algo_1, 0); 
    printf("%d %d %d", move[0], move[1], our_area());
    return 0;
}

/*
 *
 * MAKING MOVES
 *
 */

int do_move_manual(int *move)
{
    int score = -1;
    while(score < 0)
    {
        scanf("%d,%d", &move[0], &move[1]);
        printf("move received\n");
    }
    return score;
}


int do_move_algorithm(int *move)
{
    int score = 0;
    score = score + 1;
//    alpha_better(move, 1);
//    score = do_move(move);
    return(score);
}

int do_move_random(int *move)
{
    move[0] = get_random_int();
    move[1] = get_random_int();
    int score;
    while((score = do_move(move)) < 0)
    {
        move[0] = get_random_int();
        move[1] = get_random_int();
    }
    return score;
}

/*
 *
 *
 *
 */

/*
 *
 * MOVE ALGORITHMS
 *
 */

/* RANDOM ALGORITHM */
 
//Between 0 and 999 inclusive
int get_random_int()
{
    return ((int)((unsigned int) tinymt32_generate_uint32(&state) % 1000));
}
// Randomly where we don't own 
void decent_random(int *move)
{
    move[0] = get_random_int();
    move[1] = get_random_int();
    while(do_move(move) < 0 || board[move[0]][move[1]] > 0)
    {
        move[0] = get_random_int();
        move[1] = get_random_int();
    }
    undo_move(move);
}

/* */

/* ALPHA BETA */

int eval_fn()
{
    return our_area();
}

int value(int alpha, int beta, int depth, int max, int algo, int max_depth)
{
    int v = -INF, i, move[2];

    if (depth > min(max_depth, NUM_MOVES_REMAINING)){
        return eval_fn();
    }
    
    for (i = 0; i < MAX_NUMBER_OF_POINTS; i++)
    {
        if(!next_point(move, i, algo))
            break;
        if(do_move(move) > 0)
        {
            if (max)
            {
                v = max(v, value(alpha, beta, depth + 1, 0, algo, max_depth));
                if (v >= beta)
                {
                    undo_move(move);
                    return v;
                }
                alpha = max(alpha, v);
            }
            else
            {
                v = min(v, value(alpha, beta, depth + 1, 1, algo, max_depth));
                if (v <= alpha)
                {
                    undo_move(move);
                    return v;
                }
                beta = min(beta, v);
            }
            undo_move(move);
        }
    }
    return v;
}
                                 
/* Recursively realizes feasible sequences of moves and calls
 * the evaulation function
 */
void alpha_better(int *move, int algo, int max_depth)
{
    int best_v = 2 * INF, v = INF, i;
    int best_move[2];
    int max = next_to_set;

    if(max)
        best_v = -2 * INF;
     
    for (i = 0; i < MAX_NUMBER_OF_POINTS; i = i + 1)
    {
        if(!next_point(move, i, algo))
            break;
	if (do_move(move) == -1)
            continue;
        if (max)
        {
            v = value(-1 * INF, INF, 1, 0, algo, max_depth);
            if (v > best_v)
            {
                best_v = v;
                best_move[0] = move[0];
                best_move[1] = move[1];
            }
        }
        else
        {
            v = value(-1 * INF, INF, 1, 1, algo, max_depth);
            if (v < best_v)
            {
                best_v = v;
                best_move[0] = move[0]; 
                best_move[1] = move[1];
            }
        }
        undo_move(move);
    }
    move[0] = best_move[0];
    move[1] = best_move[1];
} 

