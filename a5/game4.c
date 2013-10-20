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
int do_move(int *move, int mesh);
int undo_move(int *move, int mesh);
int do_undo(int *move, int state, int mesh);
void print_board();
void decent_random(int *move);
void alpha_better(int *move);
int value(int alpha, int beta, int depth, int max, int mesh);
int eval_fn();
int our_area();

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
int NUM_MOVES_REMAINING = 4;
int MAX_NUMBER_OF_POINTS = 1000000;
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


int do_undo(int *move, int state, int mesh)
{
   int score;

   /* state 0: undo_move
    * state 1: do_move
    * state 2: do_move_manual
    */
   
   if(state == 1)
      score = do_move(move, mesh);
   else if(state == 0)
      score = undo_move(move, mesh);
   else if (state == 2)
      score = do_move_manual(move);
   return(score);   
}

int border_check(int x, int y){
  if((x<0)||(x>=BOARD_SIZE)||(y<0)||(y>=BOARD_SIZE)){
    return 0;
  }
  return 1;
}


//move is in the format [x, y] as a 2 dim array
//returns the area owned by us
int do_move(int *move, int mesh)
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
    for (i = max(move[0] - mesh, 0); i < min(BOARD_SIZE, move[0] + mesh); i++)
    {
        for (j = max(move[1] - mesh, 0); j < min(BOARD_SIZE, move[1] + mesh); j++)
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
     //Decrease number of moves remaining;
     NUM_MOVES_REMAINING--;
     return our_area;
}

void print_board()
{
    FILE *file;
    int i, j;

    file = fopen("a", "a+");
    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
            fprintf(file, "%17.16lf ", board[i][j]);
        }
        fprintf(file, "\n");
    }
    fprintf(file, "\n");
    fclose(file);
}

//move is in the format [x, y] as a 2 dim array
int undo_move(int *move, int mesh)
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
    for (i = max(move[0] - mesh, 0); i < min(BOARD_SIZE, move[0] + mesh); i++)
    {
        for (j = max(move[1] - mesh, 0); j < min(BOARD_SIZE, move[1] + mesh); j++)
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
     //Increase number of moves remaining
     NUM_MOVES_REMAINING++;
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

void test_algorithm()
{
    int p1moves[30] = {-1}, p2moves[30] = {-1};
    int i = 0, score;
    while(NUM_MOVES_REMAINING > 0)
    {
        int move[2];

        score = do_move_manual(move);
        NUM_MOVES_REMAINING++;
        p1moves[i * 2] = move[0];
        p1moves[(i * 2) + 1] = move[1];
        print_board();
        score = do_move_algorithm(move);
        printf("%d %d\n", move[0], move[1]);
        p2moves[i * 2] = move[0];
        p2moves[(i * 2) + 1] = move[1];
        print_board();
        i++;
    }
    printf("%d", our_area());
    //print_board();
    if(score <= 500000)
       save_stats(score, p1moves, p2moves);
}


int main(int argc, char *argv[])
{
//    NUM_MOVES_REMAINING = atoi(argv[1]);
//    init_board();
    int i, move[2];
    uint32_t seed = getpid();
    tinymt32_init(&state, seed);

    for(i = 0; i < 1; i++)
       test_algorithm();
    return 0;
}

int do_move_manual(int *move)
{
    int score = -1;
    while(score < 0)
    {
        scanf("%d,%d", &move[0], &move[1]);
        printf("move received\n");
        score = do_undo(move, 1, 1000);
    }
    return score;
}

// ALGORITHMS ALGORITHMS ALGORITMHS

int do_move_algorithm(int *move)
{
    int score;
    alpha_better(move);
    score = do_undo(move, 1, 1000);
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
    while((score = do_undo(move, 1, 1000)) < 0)
    {
        move[0] = get_random_int();
        move[1] = get_random_int();
    }
    return score;
}

// Randomly where we don't own 
void decent_random(int *move)
{
    int mesh = 1000;
    move[0] = get_random_int();
    move[1] = get_random_int();
    while(do_undo(move, 1, mesh) < 0 || board[move[0]][move[1]] > 0)
    {
        move[0] = get_random_int();
        move[1] = get_random_int();
    }
    do_undo(move, 0, mesh);
}

int eval_fn()
{
    return our_area();
}

int next_point(int *move, int which, int algo)
{
    int MAX_POINTS;
    if (algo == 1)
    {
        MAX_POINTS = 1000000;
        if (which > MAX_POINTS)
            return 0;
        move[0] = which / 1000;
        move[1] = which % 1000;
        return 1;
    }
    if (algo == 2)
    {
        MAX_POINTS = 525;
        if (which >= MAX_POINTS)
            return 0;
        move[0] = (which / 20) * 50;
        move[1] = (which % 20) * 50;
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
}

 int value(int alpha, int beta, int depth, int max, int mesh)
{
    int v = -INF, i, next = 0, j, move[2];
    if (depth > min(0, NUM_MOVES_REMAINING)){
        return eval_fn();
    }
    
    for (i = 0; i < MAX_NUMBER_OF_POINTS; i++)
    {
        if(!next_point(move, i, 2))
            break;
        if(do_undo(move, 1, mesh) > 0)
        {
            if (max)
            {
                v = max(v, value(alpha, beta, depth + 1, 0, mesh));
                if (v >= beta)
                {
                    do_undo(move, 0, mesh);
                    return v;
                }
                alpha = max(alpha, v);
            }
            else
            {
                v = min(v, value(alpha, beta, depth + 1, 1, mesh));
                if (v <= alpha)
                {
                    do_undo(move, 0, mesh);
                    return v;
                }
                beta = min(beta, v);
            }
            do_undo(move, 0, mesh);
        }
    }
    return v;
}
                                 
/* Recrusively realizes feasible sequences of moves and calls
 * the evaulation function
 */
void alpha_better(int *move)
{
    int best_v = 2 * INF, v = INF;
    int i, j;
    int best_move[2];
    int max = next_to_set;
    int mesh = 300;

    if(max)
        best_v = -2 * INF;
     
    for (i = 0; i < MAX_NUMBER_OF_POINTS; i = i + 1)
    {
        if(!next_point(move, i, 2))
            break;
        if (do_undo(move, 1, mesh) > 0)
        {
            if (max)
            {
                v = value(-1 * INF, INF, 1, 0, mesh);
                if (v > best_v)
                {
                    best_v = v;
                    best_move[0] = move[0];
                    best_move[1] = move[1];
                }
            }
            else
            {
                v = value(-1 * INF, INF, 1, 1, mesh);
                if (v < best_v)
                {
                    best_v = v;
                    best_move[0] = move[0]; 
                    best_move[1] = move[1];
                }
            }
            do_undo(move, 0, mesh);
        }
    }
    move[0] = best_move[0];
    move[1] = best_move[1];
} 

