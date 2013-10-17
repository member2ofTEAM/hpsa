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
void print_board();
void decent_random(int *move);

const int BOARD_SIZE = 1000;
const double INF = 10000;
double board[1000][1000];
int NUM_MOVES_REMAINING = 15;
// 1 is us, 0 is the other guy
// We assume, that we always start!
int next_to_set = 1;
tinymt32_t state;

void init_board()
{
    int i, j;
    FILE *input;
    input = fopen("input", "r");
    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
            fscanf(input, "%lf ", &board[i][j]);
        }
    }
}

double distance_squared(int x0, int y0, int x1, int y1)
{
    return (x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1);
}


//move is in the format [x, y] as a 2 dim array
//returns the area owned by us
int do_move(int *move)
{
    int our_area = 0, i, j;
    double d;
    if (move[0] < 0 || move[0] > 999 || move[1] < 0 || move[1] > 999)
        return -1;
    
    //Make sure stone can be placed
    if (abs(board[move[0]][move[1]]) == INF)
        return -1;

    //Place the stone
    if (next_to_set)
        board[move[0]][move[1]] = INF;
    else
        board[move[0]][move[1]] = -INF;

    //Update the board
    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
            d = 0.0;
            //Ignore pixels with stones set
            if (abs(board[i][j]) == INF)
                continue;
            if(move[0] == i && move[1] == j)
                continue;
            d = distance_squared(move[0], move[1], i, j);
            //If we are not next_to_set subtract the pull
            if (!next_to_set)
                d = -d;
            board[i][j] += 1.0 / d;
            //Our area only have positive pull
            if (board[i][j] > 0)
                our_area++;
        }
     }
     //Flip the player
     next_to_set = next_to_set > 0 ? 0 : 1;
     return our_area;
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

//move is in the format [x, y] as a 2 dim array
int undo_move(int *move)
{
    int our_area = 0, i, j;
    double d = 0.0;
    if (move[0] < 0 || move[0] > 999 || move[1] < 0 || move[1] > 999)
    {
        return -1;
    }
    //Make sure stone can be removed
    if (abs(board[move[0]][move[1]]) != INF)
        return -1;

    //Remove the stone
    board[move[0]][move[1]] = 0;

    //Update the board
    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
            d = distance_squared(move[0], move[1], i, j);
            if (!next_to_set)
                d = -d;
            //If the considered pixel is a placed stone, add the value to 
            //neutral pixel as appropiate
            if (abs(board[i][j]) == INF)
            {
                if(board[i][j] > 0)
                    board[move[0]][move[1]] += 1/d;
            }
            else
            {
                board[i][j] += 1 / d;
            }
            //Our area only has positive pull
            if (board[i][j] > 0)
                our_area++;
        }
     }
     //Flip the player
     next_to_set = !next_to_set;
     return our_area;
}

void save_stats(int score, int *p1moves, int *p2moves)
{
    FILE *stats;
    int i;
    stats = fopen("output.csv", "a+");
    assert(stats);
    fprintf(stats, "%d", score);
    for(i = 0; i < NUM_MOVES_REMAINING; i++)
    {
       fprintf(stats, ", %d %d", p1moves[i * 2], p1moves[(i * 2) + 1]);
       fprintf(stats, ", %d %d", p2moves[i * 2], p2moves[(i * 2) + 1]); 
    }
    fprintf(stats, "\n");
    
}

void test_algorithm()
{
    int p1moves[30] = {-1}, p2moves[30] = {-1};
    int i, score;
    for (i = 0; i < NUM_MOVES_REMAINING; i++)
    {
        int move[2];
        score = do_move_algorithm(move);
        p1moves[i * 2] = move[0];
        p1moves[(i * 2) + 1] = move[1];
        do_move_random(move);
        score = do_move_random(move);
        p2moves[i * 2] = move[0];
        p2moves[(i * 2) + 1] = move[1];
        //printf("us: %d %d; ", move[0], move[1]);
        //print_board();
        //score = do_move_random(move);
        //printf("them: %d %d; ", move[0], move[1]);
        //print_board();
        //Log results etc. - maybe use csv for sorting actions later
        //Only log if we lose?
    }
    //printf("them: %d %d; ", move[0], move[1]);
    print_board();
    if(score <= 500000)
       save_stats(score, p1moves, p2moves);
}


int main(int argc, char *argv[])
{
    //NUM_MOVES_REMAINING = atoi(argv[1]);
    //init_board();
    int i;
    uint32_t seed = getpid();
    tinymt32_init(&state, seed);

    for(i = 0; i < 5; i++)
       test_algorithm();
    return 0;
}


// ALGORITHMS ALGORITHMS ALGORITMHS

int do_move_algorithm(int *move)
{
    int score;
    decent_random(move);
    score = do_move(move);
    return(score);
}

//Between 0 and 999 inclusive
int get_random_int()
{
    return ((int)((unsigned int) tinymt32_generate_uint32(&state) % 1000));
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

int eval_fn()
{
    //can potential hack this by using the return value of do move
    int i, j, area;
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        for (int j = 0; j < BOARD_SIZE; j++)
        {
        if (board[i][j] > 0)
            area++;
        }
    }
    return area;
}

 int value(int alpha, int beta, int depth, int max)
{
    int v = -inf, i, next = 0, j;
    if (depth > 3){
        return eval_fn(0, phase);
    }
    
    for (j = 0; j < BOARD_SIZE; j++)
    {
        for (i = 0; i < BOARD_SIZE; i++)
        {
            if(do_move(i, j))
            {
                if (max)
                {
                    v = max(v, value(alpha, beta, depth + 1, 0));
                    if (v >= beta)
                    {
                        undo_move(i,j);
                        return v;
                    }
                    alpha = max(alpha, v);
                }
                else
                {
                    v = min(v, value(alpha, beta, depth + 1, 1));
                    if (v <= alpha)
                    {
                        undo_move(i,j);
                        return v;
                    }
                    beta = min(beta, v);
                }
                undo_move(i,j);
            }
         }
    }
    return v;
}
                                 
/* Recrusively realizes feasible sequences of moves and calls
 * the evaulation function
 */
void alpha_better(int *move)
{
    int best_v = -2 * INF, v = INF;
    int i, j;
    int best_move[2];
    for (j = 0; j < BOARD_SIZE; j++)
    {
        for (i = 0; i < BOARD_SIZE; i++)
        {
            if (do_move(i, j))
            {
                v = value(-1 * INF, INF, 1, 0);
                if (v > best_v)
                {
                    best_v = v;
                    best_move[0] = i;
                    best_move[1] = j;
                }
	        undo_move(i,j);
            }
        }
    }
    move[0] = best_move[0];
    printf("%d %d %d\n", best_move[0], abs(best_move[1]), best_v);
} 

