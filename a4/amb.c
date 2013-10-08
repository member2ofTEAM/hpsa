#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <inttypes.h>
#include "tinymt32.c"
#include <time.h>
#include <sys/types.h>
#include <unistd.h>

#define NUM_IN_FILE 300
#define MAX_TIME 170
#define RAND_PHEROMONE 4
#define PHEROMONE_REDUCTION 2
#define LOCAL_PHEROMONE 3
#define GLOBAL_PHEROMONE 15
#define GLOBAL_PARAMETER 50
#define MAX_ITER 500 //BEFORE CHANGING THIS, FIX BUG BELOW!!

/* patients structure */
typedef struct pat_t {
int xcoord;
int ycoord;
int life;
int claim;
int saved;
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
int no_ambu;
} hosp_t;

int savior = 0;
int max = 1;
double iterations = MAX_ITER;
double w1, w2, w3, w4;

int chooseTarget(amb_t *ant, pat_t *patients, hosp_t *hosp, int **pheromones, int mo);
int distance(int x1, int y1, int x2, int y2);
int maxPheromone(int num);
void updatePheromone(int **pheromones);
void globalPheromone(int **pheromones, int **best, int total);


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
   int i, j, k, l, life, dist, r, tmp;
   int maxi = 0;
   int count = 0, rand_tmp = 0;
   unsigned int random;
   tinymt32_t state;
   uint32_t seed = (int) getpid();
 
   tinymt32_init(&state, seed);
//   for(i = 0; i < 10; i++)
//      printf("%u ", (unsigned int) tinymt32_generate_uint32(&state));
//   printf("\n");


   /* cluster to determine where hospitals go */
   /* assign x coordinates, y coordinates of hospitals */
   /* count number of ambulances total, malloc an array of ambulances of that size */
   /* set current coordinates of all ambulances */
   /* will be amb[i] */

   savior = 0;

   file = fopen("TEAMinput.txt", "r");
   assert(file);

   /*initialize patients */
   for(i = 0; i < NUM_IN_FILE; i++)
   {
      fscanf(file, "%d", &patients[i].xcoord);
      fscanf(file, "%d", &patients[i].ycoord);
      fscanf(file, "%d", &patients[i].life);
      patients[i].claim = 0;
   }

   for(i = 0; i < 5; i++)
   {
      fscanf(file, "%d", &hosp[i].xcoord);
      fscanf(file, "%d", &hosp[i].ycoord);
      fscanf(file, "%d", &hosp[i].no_ambu);
      patients[i + NUM_IN_FILE].xcoord = hosp[i].xcoord;
      patients[i + NUM_IN_FILE].ycoord = hosp[i].ycoord;
   }

   hosp_0 = hosp[0].no_ambu;
   hosp_1 = hosp[1].no_ambu;
   hosp_2 = hosp[2].no_ambu;
   hosp_3 = hosp[3].no_ambu;
   hosp_4 = hosp[4].no_ambu;
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
      used[i] = i;
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

   

/* change this outer loop to while(TIMEVALID) */
   for(l = 0; l < iterations; l++)
   {
 
      /* ATTEMPT AT RESETTING THE VALUES
      TODO THIS IS WRONG!!!!!!!!!!! */
//IF THERE IS MORE THAN 250 ITERATOINS THIS FUCKS SHIT UP!
       if (count % 500 == 0)
       { 
           // initialize pheromone array
           for(i = 0; i < NUM_IN_FILE + 5; i++)
           {
              pheromones[i] = malloc((NUM_IN_FILE + 5) * sizeof(int));
              assert(pheromones[i]);
              for(j = 0; j < NUM_IN_FILE + 5; j++)
              {
                 random = (unsigned int) tinymt32_generate_uint32(&state);
                 random = random % RAND_PHEROMONE + 3;
                 pheromones[i][j] = random;
              }
           }
           for(i = 0; i < total; i++)
           {
               for(j = 0; j < 100; j++)
               {
                   moves[i][j] = -1;
                   best[i][j] = -1;
               }
           }
      }   

//CHANGE THE BEHAVIOR WITH THIS
//THERE ARE FOUR BEHAVIOR PATTERNS
//SWITCH TO THE NEXT ONE HERE
//GO THROUGH ALL FOUR
//HARDCORE THEM!!

     if(count % 500 == 0)
     {
         random = (unsigned int) tinymt32_generate_uint32(&state);
         random = random % 23429783;
         w1 = (double) random / 23429783.0;
//         w1 = 0.7 + 0.2*w1;
         random = (unsigned int) tinymt32_generate_uint32(&state);
         random = random % 243081;
         w2 = (double) random / 243081.0; 
//         w2 = 0.5 + 0.1*w2;
         random = (unsigned int) tinymt32_generate_uint32(&state);
         random = random % 97834897;
         w3 = (double) random / 97834897.0;
//         w3 = 0.6 + 0.1*w3;
         random = (unsigned int) tinymt32_generate_uint32(&state);
         random = random % 8273493;
         w4 =  (double) random / 8273493.0;
//         w4 = 0.4 + 0.2*w4;
         fprintf(stderr, "%f %f %f %f\n", w1, w2, w3, w4);
      }
      for(k = total - 1; k > -1; k--)
         {
            random = (unsigned int) tinymt32_generate_uint32(&state);
            random = random % total;
            rand_tmp = (int)random;
            tmp = used[k];
            used[k] = used[rand_tmp];
            used[rand_tmp] = tmp;
         }
      
      for(i = 0; i < total; i++)
      {
         r = used[i];
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
         ant.next = amb[r].hospital + NUM_IN_FILE;
         k = 0;
         j = 0;
         while(j != 2)
         {
      //     if (used[i] == 4 || used[i] == 12 || used[i] == 18 || used[i] == 25 || used[i] == 35
      //       ||used[i] == 3 || used[i] == 11 || used[i] == 17 || used[i] == 24 || used[i] == 34
      //       ||used[i] == 2 || used[i] == 10 || used[i] == 16 || used[i] == 23 || used[i] == 33)
      //         break;
            j = chooseTarget(&ant, patients, hosp, pheromones, r);
            moves[r][k] = ant.next; 
            k = k + 1;  
         }
      }
       
      /* reset array (may not be necessary */
      for(i = 0; i < total; i++)
         used[i] = i;

      /* check to see if this solution is better. If so, save it */
      if(maxi < savior)
      {
         maxi = savior;
         for(i = 0; i < total; i++)
         {
            for(j = 0; j < 100; j++)
            {
                best[i][j] = -1;
                best[i][j] = moves[i][j]; /* store best */
            }
            amb[i].chosen = 0; /* make them no longer chosen */
         }
      }

      for (i = 0; i < total; i++)
      {
          for (j = 0; j < 100; j++)
              moves[i][j] = -1;
      }
      
    
      /* reset savior and claimed patients */
      savior = 0;
      for(i = 0; i < NUM_IN_FILE; i++)
         patients[i].claim = 0;
   
      count++;
      if(count % GLOBAL_PARAMETER == 0)
      {
         /* reinforce current known best */
         globalPheromone(pheromones, best, total);
      }
      updatePheromone(pheromones); /* update local pheromones */

   }
      int pat[4], hospt;     
      pat[0] = 0; pat[1] = 0; pat[2] = 0; pat[3] = 0; 
   /* Print ambulances */
      for (i = 0; i < total; i ++)
      {
          j = 0;
          k = 0;
          while (best[i][j] >= 0)
          {
              if(best[i][j] >= 300)
              {
                  hospt = best[i][j];
                 if (pat[3] != -1)
                      printf("ambulance %d %d (%d, %d, %d); %d (%d, %d, %d); %d (%d, %d, %d); %d (%d, %d, %d); (%d, %d)\n", i, 
								 pat[0], patients[pat[0]].xcoord, patients[pat[0]].ycoord, patients[pat[0]].life,
                                                                 pat[1], patients[pat[1]].xcoord, patients[pat[1]].ycoord, patients[pat[1]].life,
								 pat[2], patients[pat[2]].xcoord, patients[pat[2]].ycoord, patients[pat[2]].life, 
								 pat[3], patients[pat[3]].xcoord, patients[pat[3]].ycoord, patients[pat[3]].life, 
								 patients[hospt].xcoord, patients[hospt].ycoord);

                  else if (pat[2] != -1)
                      printf("ambulance %d %d (%d, %d, %d); %d (%d, %d, %d); %d (%d, %d, %d); (%d, %d)\n", i, 
								 pat[0], patients[pat[0]].xcoord, patients[pat[0]].ycoord, patients[pat[0]].life,
                                                                 pat[1], patients[pat[1]].xcoord, patients[pat[1]].ycoord, patients[pat[1]].life,
								 pat[2], patients[pat[2]].xcoord, patients[pat[2]].ycoord, patients[pat[2]].life, 
								 patients[hospt].xcoord, patients[hospt].ycoord);

                  else if (pat[1] != -1)
                      printf("ambulance %d %d (%d, %d, %d); %d (%d, %d, %d); (%d, %d)\n", i,
								 pat[0], patients[pat[0]].xcoord, patients[pat[0]].ycoord, patients[pat[0]].life,
                                                                 pat[1], patients[pat[1]].xcoord, patients[pat[1]].ycoord, patients[pat[1]].life,
								 patients[hospt].xcoord, patients[hospt].ycoord);

                  else if (pat[0] != -1)
                      printf("ambulance %d %d (%d, %d, %d); (%d, %d)\n", i,
                                                                 pat[0], patients[pat[0]].xcoord, patients[pat[0]].ycoord, patients[pat[0]].life,
								 patients[hospt].xcoord, patients[hospt].ycoord);
                   for (k = 0; k < 4; k++)
                      pat[k] = -1;
                   k = 0;
 
               }
               else
               {
                   pat[k] = best[i][j];
                   k = k + 1;
               }
               j = j + 1;
          } 
      }  
   printf("%d", maxi);

   /* free all arrays */
   for(i = 0; i < total; i++)
   {
      free(moves[i]);  
      free(best[i]); 
   } 
   free(moves);
   free(best);
   free(used); 

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
int chooseTarget(amb_t *ant, pat_t *patients, hosp_t *hosp, int **pheromones, int mo)
{
   int i, j, r, p, bestd = 10000, bestd2, best, dist, dist1, dist2, bestd1;
   double score = 0, bestscore = 0;
   int flag = 0;
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
//<<<<<<< HEAD
 //               if((patients[ant->pat1].life - ant->time) < dist1 + bestd2 + 2)
/*=======*/
                if((patients[ant->pat1].life - ant->time - dist1 - bestd2 - 2)<0)
//>>>>>>> d9c7dbe446cc39abba2067e01be2fbb9eb747eca
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
         
               p = pheromones[i][ant->next];

               score  = w1 * ((double)(200 - dist1) / 200.0); 
               score += w2 * ((double)(MAX_TIME - patients[i].life) / (double) MAX_TIME);
               score += w3 * ((double)p/(double)max);
               score += w4 * ((iterations - (double) patients[i].saved) / iterations);
         
               if(score >= bestscore)
               {
                  bestd1 = dist1;
                  bestscore = score;
                  best = i; 
               } 

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
         max = maxPheromone(pheromones[best][ant->next]);

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

         if(ant->pat4 != -1)
            patients[ant->pat4].saved++;
         if(ant->pat3 != -1)
            patients[ant->pat3].saved++;
         if(ant->pat2 != -1)
            patients[ant->pat2].saved++;
         if(ant->pat1 != -1)
            patients[ant->pat1].saved++;


    
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


int maxPheromone(int pheromone)
{
   if(max < pheromone)
      max = pheromone;
   if(max < 1)
      max = 1;
   return(max); 
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

   for(i = 0; i < NUM_IN_FILE + 5; i++)
   {
      for(j = 0; j < NUM_IN_FILE + 5; j++)
      {
         if(pheromones[i][j] > 1)
            pheromones[i][j] = pheromones[i][j] - PHEROMONE_REDUCTION;
         if(pheromones[i][j] == 1)
            pheromones[i][j] = 0;
      }
   }
   /* reduce pheromones */
} /* end of updatePheromone */



void globalPheromone(int **pheromones, int **best, int total)
{
   int i, j;

   for(i = 0; i < total; i++)
   {
      j = 0;
      while(best[i][j] != -1 && best[i][j+1] != -1)
      {
         pheromones[best[i][j]][best[i][j+1]] += GLOBAL_PHEROMONE;
         pheromones[best[i][j+1]][best[i][j]] += GLOBAL_PHEROMONE;
         j++;
      }
   }

}

