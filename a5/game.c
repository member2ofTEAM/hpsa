#include <stdio.h>

int BOARD_SIZE = 1000;
double board[BOARD_SIZE][BOARD_SIZE];
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

//move is in the format [x, y] as a 2 dim array
void do_move(int *move)
{
    
}

void undo_move(int *move)
{

}

int main()
{
    init_board();
    test_algorithm();
    return 0;
}

void test_algorithm()
{
    int i;
    for (i = 0; i < 20; i++)
    {
        do_move(get_move_algorithm());
        do_move(get_move_random());
        //Log results etc. - maybe use csv for sorting actions later
        //Only log if we lose?
    }
}

int *get_move_algorithm()
{

}

int *get_move_random()
{

}


