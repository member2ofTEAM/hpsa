#include <stdio.h>
#include "tinymt32.h"
#include <stdlib.h>
#include <math.h>
#include <sys/types.h>
#include <unistd.h>
#include "tinymt32.c"
#include <time.h>

void test_algorithm();
int do_move_random(int *move);
void print_board();

const int BOARD_SIZE = 1000;
const double INF = 10000;
double board[1000][1000];
// 1 is us, 0 is the other guy
// We assume, that we always start!
int next_to_set = 1;

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
            if (i == j)
                continue;
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

void test_algorithm()
{
    int i, score;
    for (i = 0; i < 1; i++)
    {
        int move[2];
        do_move_random(move);
        //printf("us: %d %d; ", move[0], move[1]);
        print_board();
        score = do_move_random(move);
        //printf("them: %d %d; ", move[0], move[1]);
        print_board();
        //Log results etc. - maybe use csv for sorting actions later
        //Only log if we lose?
    }
    printf("Final score: %d\n", score);

}

int main()
{
    //init_board();
    test_algorithm();
    return 0;
}

void do_move_algorithm(int *move)
{
    int i;
    i = i + 1;
}

//Between 0 and 999 inclusive
int get_random_int()
{
    return (int) (rand() % 1000);
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



