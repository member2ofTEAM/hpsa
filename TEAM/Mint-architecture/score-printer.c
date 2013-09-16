#include "utils.h"

/* Expects input of the form
Score Team_name Additional information
 */

typedef struct {
	char *team_name;
	int score;
} Team;

int compare(const void *t1, const void *t2);
void parse(char *str, Team *scores, int *index);

int main(int argc, char *argv[])
{
	int num_teams = 0, i = 32, rank_tied;
	char *line = NULL;
	Team *scores = (Team*) xmalloc(32 * sizeof(Team));

	/* While we can still read a line from stdin */
	while((line = readLine(stdin)) != NULL) {
		parse(line, scores, &num_teams);
		/* if we need more memory, double the size of the array */
		if(++num_teams == i)
			scores = (Team*) xrealloc(scores, (i <<= 1) * sizeof(Team));
		free(line);
	}

	puts("   RANK   |     SCORE     |    VALUATIONS    | TEAM NAME\n"
	     "----------+---------------+-----------------------------------------------------");
	if(num_teams > 0) {
		/* sort teams from best to worst */
		qsort(scores, num_teams, sizeof(Team), &compare);

		/* if multiple teams have the same score, we give them the same rank */
		rank_tied = 0;
		for(i = 0; i < num_teams; i++) {
			if(scores[i].score != scores[rank_tied].score)
				rank_tied = i;
			printf("%9d | %13d | %s\n", rank_tied + 1, scores[i].score, scores[i].team_name);
		}
	}
	free(scores);

	return 0;
}

/* Orders scores in ascending order when passed to qsort.
 * To order scores in descending order, swap 1 with -1
 * See 'qsort' manpage for more details */
int compare(const void *t1, const void *t2)
{
	return ((Team*) t1)->score == ((Team*) t2)->score ? 0 :
		(((Team*) t1)->score > ((Team*) t2)->score ? 1 : -1);
}

/* parse str into a Team structure and add it to the scores array */
void parse(char *str, Team *scores, int *index)
{
	int i;
	/* advance till we hit a non-digit in the string */
	for(i = 0; isdigit(str[i]); i++)
		;
	if(i == 0 || str[i] == '\0') {
		fprintf(stderr, "Invalid line '%s'.\n", str);
		(*index)--;
	} else {
		/* make the first non-digit string a separator between score and team name. Parse */
		str[i] = '\0';
		scores[*index].score = atoi(str);
		scores[*index].team_name = (char*) xstrdup(str + i + 1);
	}
}
