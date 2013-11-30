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
void final_best_move(int *move, int algo);
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
                                                                    
    //TODO NEED TO FLIP NEXT_TO_SET AS MANY TIMES AS THERE ARE MOVES!
    for (i = 0; i < MAX_NUMBER_OF_POINTS; i++)
    {
        if (!next_point(pos, i, 1))
            break;
        if(abs(board[pos[0]][pos[1]]) != INF)
            board[pos[0]][pos[1]] = exact_pull(pos);
    }

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

int next_point(int *move, int which, int algo)
{
    int MAX_POINTS;
    int x, y;

    if (algo == 1)
    {
        MAX_POINTS = 10000;
        if (which >= MAX_POINTS)
            return 0;
        move[0] = (which / 100) * 10;
        move[1] = (which % 100) * 10;
        return 1;
    }
    return 0;
}

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
    final_best_move(move, 1);
    while(abs(board[move[0]][move[1]]) == INF)
    {
       move[0] = get_random_int() % 1000;
       move[1] = get_random_int() % 1000;
    }
    printf("%d %d %d", move[0], move[1], our_area());
    return 0;
}

//Between 0 and 999 inclusive
int get_random_int()
{
    return ((int)((unsigned int) tinymt32_generate_uint32(&state) % 1000));
}

/* */
void final_best_move(int *move, int algo)
{
    int best_v = -1, i, v;
    int best_move[2];

    for (i = 0; i < MAX_NUMBER_OF_POINTS; i = i + 1)
    {
        if(!next_point(move, i, algo))
            break;
    	if (do_move(move) == -1)
            continue;
        v = our_area();
        if (v < best_v)
        {
            best_v = v;
            best_move[0] = move[0]; 
            best_move[1] = move[1];
        }
        undo_move(move);
    }
    move[0] = best_move[0];
    move[1] = best_move[1];
} 

