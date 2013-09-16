#include "utils.h"
#include <limits.h>

//#define DEBUG		// uncomment to print array

#define array(i)	((i) < 1 ? INT_MAX : array[i]) 
#define minimum(m1, m2, m3, m4, m5)	min(min(m1, m2), min(min(m3, m4), m5))

unsigned min(unsigned a, unsigned b);
void parse(char *str, int valuations[]);
unsigned score(unsigned array[], int N);
void fill_array_exact_change(unsigned array[], int valuations[]);
void fill_array_exchange(unsigned array[], int valuations[]);

int main(int argc, char *argv[])
{
	int i, N, valuations[5], probnum;
	unsigned array[105] = { 0 };
	char *line = NULL, *team_name = NULL;

	if(argc != 3) {
		fprintf(stderr, "Usage: %s N problem-number.\n", argv[0]);
		return 0;
	}

	/* get value of N and determine which problem to solve */
	N = atoi(argv[1]);
	if((probnum = atoi(argv[2])) != 1 && probnum != 2) {
		fputs("Invalid problem number.\n", stderr);
		exit(EXIT_FAILURE);
	}

	/* read 2 lines and exit if no lines to be read */
	if((team_name = readLine(stdin)) == NULL || (line = readLine(stdin)) == NULL) {
		fputs("Error reading input. Exiting now…\n", stderr);
		exit(EXIT_FAILURE);
	}

	parse(line, valuations);
	free(line);

	/* fill array and print score */
	switch(probnum) {
		case 1:
			fill_array_exact_change(array, valuations);
			break;
		case 2:
			fill_array_exchange(array, valuations);
	}

#ifdef DEBUG
	for(i = 1; i < 101; i++)
		printf("array[%d]: %u\n", i, array[i]);
#endif

	printf("%u (%2d %2d %2d %2d %2d) | %s\n", score(array, N), valuations[0], valuations[1],
			valuations[2], valuations[3], valuations[4], team_name);
	free(team_name);

	return 0;
}

int contains(int* valuations, int i)
{
	if(i == valuations[0] || i == valuations[1] || i == valuations[2] || i == valuations[3] || i == valuations[4] || i == 100)
		return 1;
	else
		return 0;
}

void fill_array_exact_change(unsigned array[], int valuations[])
{
	int i;
	for(i = 1; i < 105; i++)
		array[i] = INT_MAX;
	
	for(i = 0; i < 5; i++)
		array[valuations[i]] = 1;
	array[100] = 0;

	for(i = 1; i < 105; i++)
		if(contains(valuations, i))
			continue;
		else
			array[i] = minimum(array(i - valuations[0]), array(i - valuations[1]), array(i - valuations[2]),
					array(i - valuations[3]), array(i - valuations[4])) + 1;
}

void fill_array_exchange(unsigned array2[], int valuations[])
{
	int i, j;
	unsigned array[105];

	for(i = 1; i < 105; i++)
		array2[i] = array[i] = INT_MAX;

	for(i = 0; i < 5; i++)
		array2[valuations[i]] = array[valuations[i]] = 1;
	array2[100] = array[100] = 0;

	fill_array_exact_change(array, valuations);
	for(i = 1; i < 100; i++)
		if(contains(valuations, i))
			continue;
		else
			for(j = i + 1; j < 105; j++)
				array2[i] = min(array2[i], min(array[i], array[j] + array[j-i]));
}

unsigned min(unsigned a, unsigned b)
{
	return a < b ? a : b;
}

unsigned score(unsigned array[], int N)
{
	unsigned total = 0;
	int i;

	for(i = 1; i < 101; i++) {
		if((i + 1) % 5)
			total += array[i];
		else
			total += array[i] * N;
	}
	return total;
}

/* parse input line into valuations array. */
void parse(char *str, int valuations[])
{
	int i, count = 0;

	for(i = 0; str[i] != '\0' && count < 5; i++)
		/* whenever we hit a space, parse the number */
		if(str[i] == ' ') {
			str[i] = '\0';
			valuations[count++] = atoi(str);
			str += i + 1;
			i = -1;
		}

	/* if invalid line */
	if(count != 4) {
		fputs("Error: invalid line.\n", stderr);
		exit(EXIT_FAILURE);
	}
	/* we parsed all the numbers except the last one. Do it here */
	valuations[4] = atoi(str);
}

