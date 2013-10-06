#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>

#define NUM_IN_FILE 300
#define MAX_TIME 170
#define PHEROMONE_REDUCTION 1
#define LOCAL_PHEROMONE 5
#define GLOBAL_PHEROMONE 35
#define GLOBAL_PARAMETER 20

/* patients structure */
typedef struct pat_t {
int xcoord;
int ycoord;
int life;
int claim;
} pat_t;

/* ambulances */
typedef struct amb_t {
int xcoord;
int ycoord;
int next;  /* this is actually current */
int chosen;
int time;
int pat1;
int pat2;
int pat3;
int pat4;
int hospital;
} amb_t;

/* hospitals */
typedef struct hosp_t {
int xcoord;
int ycoord;
} hosp_t;

int savior = 0;

int main(int argc, char *argv[])
{
   pat_t patients[NUM_IN_FILE + 10];
   hosp_t hosp[5];
   amb_t *amb;
   amb_t ant;
   int hosp_0, hosp_1, hosp_2, hosp_3, hosp_4, total, test1, test2;
   int **moves;
   int **best;
   int *used;
   FILE *file;
   int **pheromones;
   int i, j, k, l, life, dist, r;
   int max = 0;
   int count = 0;

   /* cluster to determine where hospitals go */
   /* assign x coordinates, y coordinates of hospitals */
   /* count number of ambulances total, malloc an array of ambulances of that size */
   /* set current coordinates of all ambulances */
   /* will be amb[i] */

   savior = 0;
   /* UPDATE THIS! */
   hosp[0].xcoord = 49;
   hosp[0].ycoord = 25;
   hosp_0 = 5;
   hosp[1].xcoord = 27;
   hosp[1].ycoord = 77;
   hosp_1 = 9;
   hosp[2].xcoord = 78;
   hosp[2].ycoord = 75;
   hosp_2 = 6;
   hosp[3].xcoord = 15;
   hosp[3].ycoord = 32;
   hosp_3 = 11;
   hosp[4].xcoord = 84;
   hosp[4].ycoord = 26;
   hosp_4 = 10;
   total = hosp_0 + hosp_1 + hosp_2 + hosp_3 + hosp_4;


   moves = malloc(total * sizeof(int*));
   assert(moves);
   best = malloc(total * sizeof(int*));
   assert(best);
   used = malloc(total * sizeof(int));
   assert(used);

   for(i = 0; i < total; i++)
   {
      moves[i] = malloc(100 * sizeof(int));
      assert(moves[i]);
      best[i] = malloc(100 * sizeof(int));
      assert(moves[i]);
      for(j = 0; j < 100; j++)
      {
         moves[i][j] = -1;
         best[i][j] = -1;
      }
      used[i] = 0;
   }

   
   pheromones = malloc((NUM_IN_FILE + 5) * sizeof(int*)); /* pheromones between patients and hospitals */
   assert(pheromones);
   amb = malloc(total * sizeof(amb_t));
   assert(amb);



   /* initialization of ambulances */
   for(i = 0; i < total; i++)
   {
      amb[i].chosen = 0;
      amb[i].time = 0;
      amb[i].next = -1;
      amb[i].pat1 = -1;
      amb[i].pat2 = -1;
      amb[i].pat3 = -1;
      amb[i].pat4 = -1;
   }

   for(i = 0; i < hosp_0; i++)
   {
      amb[i].xcoord = hosp[0].xcoord;
      amb[i].ycoord = hosp[0].ycoord;
      amb[i].hospital = 0;
      amb[i].next = NUM_IN_FILE + 0;
   }
   for(i = 0; i < hosp_1; i++)
   {
      amb[i + hosp_0].xcoord = hosp[1].xcoord;
      amb[i + hosp_0].ycoord = hosp[1].ycoord;
      amb[i + hosp_0].hospital = 1;
      amb[i + hosp_0].next = NUM_IN_FILE + 1;
   }
   for(i = 0; i < hosp_2; i++)
   {
      amb[i + hosp_0 + hosp_1].xcoord = hosp[2].xcoord;
      amb[i + hosp_0 + hosp_1].ycoord = hosp[2].ycoord;
      amb[i + hosp_0 + hosp_1].hospital = 2;
      amb[i + hosp_0 + hosp_1].next = NUM_IN_FILE + 2;
   }
   for(i = 0; i < hosp_3; i++)
   {
      amb[i + hosp_0 + hosp_1 + hosp_2].xcoord = hosp[3].xcoord;
      amb[i + hosp_0 + hosp_1 + hosp_2].ycoord = hosp[3].ycoord;
      amb[i + hosp_0 + hosp_1 + hosp_2].hospital = 3;
      amb[i + hosp_0 + hosp_1 + hosp_2].next = NUM_IN_FILE + 3;
   }
   for(i = 0; i < hosp_4; i++)
   {
      amb[i + hosp_0 + hosp_1 + hosp_2 + hosp_3].xcoord = hosp[4].xcoord;
      amb[i + hosp_0 + hosp_1 + hosp_2 + hosp_3].ycoord = hosp[4].ycoord;
      amb[i + hosp_0 + hosp_1 + hosp_2 + hosp_3].hospital = 4;
      amb[i + hosp_0 + hosp_1 + hosp_2 + hosp_3].next = NUM_IN_FILE + 4;
   }

   
   /* initialize pheromone array */
   for(i = 0; i < NUM_IN_FILE + 5; i++)
   {
      pheromones[i] = malloc((NUM_IN_FILE + 5) * sizeof(int));
      assert(pheromones[i]);
      for(j = 0; j < NUM_IN_FILE + 5; j++)
         pheromones[i][j] = 0;
   }
  
   file = fopen("ambu2009.txt", "r");
   assert(file);

   /* initialize patients and grid */
   for(i = 0; i < NUM_IN_FILE; i++)
   {
      fscanf(file, "%d", &patients[i].xcoord);
      fscanf(file, "%d", &patients[i].ycoord);
      fscanf(file, "%d", &patients[i].life);
      patients[i].claim = 0;
   }
   
   for(i = 0; i < 5; i++)
   {
      patients[i + NUM_IN_FILE].xcoord = hosp[i].xcoord;
      patients[i + NUM_IN_FILE].ycoord = hosp[i].ycoord;
   }


/* change this outer loop to while(TIMEVALID) */
   for(l = 0; l < 1; l++)
   {
      for(i = 0; i < total; i++)
      {
         while(1)
         {
            /* UPDATE THIS TO BE FASTER AT CHOOSING ONE THAT HASN'T BEEN CHOSEN */            
           /* srand(time(NULL));
         a   r = rand() % total;
            if(used[r] != 1)
            {
               used[r] = 1;
               break;
            } 
             GENERATE RANDOM NUMBER BETWEEN 0 AND total. CALL IT r */
            /* only use non chosen ants. Break when successful. */
            r = i;
            break;
         }
         amb[r].chosen = 1;  //reset these outside for loop 
         ant.xcoord = amb[r].xcoord;
         ant.ycoord = amb[r].ycoord;
         ant.chosen = amb[r].chosen;
         ant.hospital = amb[r].hospital; 
         ant.time = 0;
         ant.pat1 = -1;
         ant.pat2 = -1;
         ant.pat3 = -1;
         ant.pat4 = -1;
         ant.next = ant.hospital + NUM_IN_FILE;
         k = 0;
         j = 0;
         while(j != 2)
         {
            j = chooseTarget(&ant, patients, hosp, pheromones);
            moves[i][k] = ant.next; 
            k = k + 1;
            if (ant.pat4 != -1)
               printf("Ambulance %d %d (%d, %d, %d); %d (%d, %d, %d); %d (%d, %d, %d); %d (%d, %d, %d)\n", r, 
                                                                 ant.pat1, patients[ant.pat1].xcoord, patients[ant.pat1].ycoord, patients[ant.pat1].life,
								 ant.pat2, patients[ant.pat2].xcoord, patients[ant.pat2].ycoord, patients[ant.pat2].life, 
								 ant.pat3, patients[ant.pat3].xcoord, patients[ant.pat3].ycoord, patients[ant.pat3].life, 
								 ant.pat4, patients[ant.pat4].xcoord, patients[ant.pat4].ycoord, patients[ant.pat4].life);

            else if (ant.pat3 != -1)
               printf("Ambulance %d %d (%d, %d, %d); %d (%d, %d, %d); %d (%d, %d, %d)\n", r, 
                                                                 ant.pat1, patients[ant.pat1].xcoord, patients[ant.pat1].ycoord, patients[ant.pat1].life,
								 ant.pat2, patients[ant.pat2].xcoord, patients[ant.pat2].ycoord, patients[ant.pat2].life, 
								 ant.pat3, patients[ant.pat3].xcoord, patients[ant.pat3].ycoord, patients[ant.pat3].life); 

            else if (ant.pat2 != -1)
               printf("Ambulance %d %d (%d, %d, %d); %d (%d, %d, %d)\n", r, 
                                                                 ant.pat1, patients[ant.pat1].xcoord, patients[ant.pat1].ycoord, patients[ant.pat1].life,
								 ant.pat2, patients[ant.pat2].xcoord, patients[ant.pat2].ycoord, patients[ant.pat2].life);

           else if (ant.pat1 != -1)
               printf("Ambulance %d %d (%d, %d, %d)\n", r, 
                                                                 ant.pat1, patients[ant.pat1].xcoord, patients[ant.pat1].ycoord, patients[ant.pat1].life);

         }
  //       for(j = 0; j < 10; j++)
    //        printf("%d ", moves[i][j]);
      }
       
      /* reset used */

      /* check to see if this solution is better. If so, save it */
      if(max < savior)
      {
         max = savior;
         for(i = 0; i < total; i++)
         {
            for(j = 0; j < 100; j++)
            {
               best[i][j] = moves[i][k]; /* store best */
               moves[i][k] = -1; /* reset moves */
            }
            amb[i].chosen = 0; /* make them no longer chosen */
         }
      }
      /* reset savior and claimed patients */
      savior = 0;
      for(i = 0; i < NUM_IN_FILE; i++)
         patients[i].claim = 0;
   
      count++;
      if(count % GLOBAL_PARAMETER == 0)
      {
         /* reinforce current known best */
      }

   /*   updatePheromones(pheromones); */ /* update local pheromones */

   }

   printf("SAVED = %d\n", max);


   /* FREE MOVES AND BEST */

   /* free all arrays */
   for(i = 0; i < NUM_IN_FILE + 5; i++)
      free(pheromones[i]);
   free(pheromones);
   free(amb);
   fclose(file);

   return (0);
} /* end of main */


/* returns 0 if a new patient was selected successfully. Returns 1 if
 * it just visited a hospital, thus indicating it needs a new patient
 * Returns 2 if time ran out. */
int chooseTarget(amb_t *ant, pat_t *patients, hosp_t *hosp, int **pheromones)
{
   int i, j, r, bestd = 10000, bestd2, best, dist, dist1, dist2, bestd1;
   int score = 0, bestscore = 0, flag = 0;
   int pat_num = 0;


   if(ant->pat1 != -1)
      pat_num++;
   if(ant->pat2 != -1)
      pat_num++;
   if(ant->pat3 != -1)
      pat_num++;
   if(ant->pat4 != -1)
      pat_num++;    


   best = -1;

   if(ant->time > MAX_TIME)
      return(2);

   
   /* makes sure a space is open */
   if(pat_num < 4/*&& (ant->time < MAX_TIME)*/)
   {
      bestd1 = 100000;
      /* checks remaining possible */
      for(i = 0; i < NUM_IN_FILE; i++)
      {
         /* ensures it hasn't been used */
         if(!patients[i].claim)
         {
            /* checks distance to new patient */
            dist1 = distance(ant->xcoord, ant->ycoord, patients[i].xcoord, patients[i].ycoord);
            bestd2 = 100000;
            for(j = 0; j < 5; j++)
            {
               /* gets distance from new patient to nearest hospital */
               dist2 = distance(patients[i].xcoord, patients[i].ycoord, hosp[j].xcoord, hosp[j].ycoord);
               if(dist2 < bestd2)
                  bestd2 = dist2;
            }
            /* ensures new patient could make it to a hospital */
            if((patients[i].life - ant->time - dist1 - bestd2 - 2)>0)
            {
               /* ensures all other ants can still make it back given the new ant is picked up  */
              if(ant->pat1 != -1)
               {
                if((patients[ant->pat1].life - ant->time - dist1 - bestd2 - 2)<0)
                     continue;
               } 
              if(ant->pat2 != -1)
               {
                  if((patients[ant->pat2].life - ant->time - dist1 - bestd2 -2)<0)
                     continue;
               }
               if(ant->pat3 != -1)
               {
                  if((patients[ant->pat3].life - ant->time - dist1 - bestd2 -2)<0)
                     continue;
               }
              
               
              if((ant->time + dist1 + bestd2 + 2 )> MAX_TIME)
                  continue;

               if(dist1 <= bestd1)
               {
                  bestd1 = dist1;
                  best = i;
               }
                  
                  
               /* SCORING */


               /* save best score and index of that ant */
               /*
               if(score > bestscore)
               {
                  bestd = dist1;
                  bestscore = score;
                  best = i; 
               }
               */

            }
         }  
      }
 
      /* if no best is found, go to hospital */
      if(best == -1)
      {
         if(pat_num > 0)
            flag = 1;
         else
            return(2);
      }
      else /* otherwise, update ant, pheromones, and claim patient */
      {
         if(ant->pat1 == -1)
            ant->pat1 = best;
         else if(ant->pat2 == -1)
            ant->pat2 = best;
         else if(ant->pat3 == -1)
            ant->pat3 = best;
         else
            ant->pat4 = best;
         pheromones[ant->next][best] += LOCAL_PHEROMONE; /* update pheromones */
         pheromones[best][ant->next] += LOCAL_PHEROMONE;

         ant->time = ant->time + bestd1 + 1; /* update time */
         ant->next = best; /* current patient */
         ant->xcoord = patients[best].xcoord; /* move ant */
         ant->ycoord = patients[best].ycoord;
         patients[best].claim = 1; /* claim new patient */
         return(0); /* picked up a patient */
      }
   }
   /* if full, go to hospital if time is not exceeded. Else stop */
   else 
   {
      if(ant->time < MAX_TIME)
         flag = 1;
      else
         return(2);
   }


   /* if it has to go back to a hospital, go to the closest one, update
    * "next" target, reset patients, add their count to savior (if they were
    * saved), removes time from this ant. Returns 1 if it went to hospital
    * successfully, 2 if time ran out
    * */
   if(flag)
   {
      /* if it is already at a hospital, stop */
      if((ant->next == NUM_IN_FILE) || (ant->next == NUM_IN_FILE + 1) || (ant->next == NUM_IN_FILE + 2)              || (ant->next == NUM_IN_FILE + 3) || (ant->next == NUM_IN_FILE + 4))
            return(2);

      bestd = 10000;
      for(i = 0; i < 5; i++)
      {
         /* finds closest hospital */
         dist = distance(ant->xcoord, ant->ycoord, hosp[i].xcoord, hosp[i].ycoord);
         if(dist < bestd)
         {
            bestd = dist;
            best = i;
         }
      }
      /* ensures time will be enough */
      if(ant->time + bestd + 1 < MAX_TIME)
      {
         ant->xcoord = hosp[best].xcoord; /* moves ant */
         ant->ycoord = hosp[best].ycoord;

         savior += pat_num;

         /* saves patients */
 /*        if(ant->pat1 != -1)
         {
            if(patients[ant->pat1].life - bestd - ant->time - 1 > -1)
               savior++;
         }
         if(ant->pat2 != -1)
         {
            if(patients[ant->pat2].life - bestd - ant->time - 1 > -1)
               savior++;
         }
         if(ant->pat3 != -1)
         {
            if(patients[ant->pat3].life - bestd - ant->time - 1 > -1)
               savior++;
         }
         if(ant->pat4 != -1)
         {
            if(patients[ant->pat4].life - bestd - ant->time - 1 > -1)
               savior++;
         } */
       
         ant->pat1 = -1; /* empties ambulance */
         ant->pat2 = -1;
         ant->pat3 = -1;
         ant->pat4 = -1;
         ant->time = ant->time + bestd + 1; /* update time */
         pheromones[ant->next][best + NUM_IN_FILE] += LOCAL_PHEROMONE; /* place pheromones */
         pheromones[best + NUM_IN_FILE][ant->next] += LOCAL_PHEROMONE;
         ant->next = best + NUM_IN_FILE; /* ant is at hospital */
         ant->xcoord = hosp[best].xcoord;
         ant->ycoord = hosp[best].ycoord;
         return(1);
      }
      else
      {
         ant->time = MAX_TIME + 10; /* didn't have enough time */
         return(2);
      }
   }
   return(2);

}


/* calculates distance between 2 points */
int distance(int x1, int y1, int x2, int y2)
{
   int dist;
   dist = abs(x1 - x2) + abs(y1 - y2);
   return (dist);
}

/* Pheromones will be set to 3-10 when they are placed (number
 * subject to change) and will be reduced by 1 after an ant
 * explores a path. This will allow ants to have a small bias
 * towards paths that have already been explored, but not
 * so much as to not explore that path again. When the best
 * path has been found, */
void updatePheromone(int **pheromones)
{
   int i, j;


   /* reduce pheromones */
} /* end of updatePheromone */


