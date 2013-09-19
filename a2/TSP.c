#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

int main(int argc, char *argv[])
{
   FILE *file;
   int **city, *order, *best;
   int i, j, k, i_ind, j_ind, ind1, ind2, tmp, min1 = 1000000, min2 = 100000;
   double min, sum, bests, check;
   double **dist;
   double Distance(int *a, int *b);
   double totalDistance(int *order, int **city);
   void eTest(int *order);
   void printSequence(int *order);
   void arrayCopy(int *order, int *best);

   min = 1000000000.0;
   bests = 100000000.0;
   sum = 0.0;

   order = malloc(1000 * sizeof(int));
   assert(order);
   best = malloc(1000 * sizeof(int));
   assert(best);
   city = malloc(1000 * sizeof(int*));
   assert(city);
   dist = malloc(1000 * sizeof(double*));
   assert(dist);
   file = fopen(argv[1], "r");
   assert(file);

   /* fill in city array from file */
   for(i = 0; i < 1000; i++)
   {
      city[i] = malloc(4 * sizeof(int));
      assert(city[i]);
      dist[i] = malloc(1000 * sizeof(double));
      assert(dist[i]);   
      fscanf(file, "%d %d %d %d", &city[i][0], &city[i][1], &city[i][2], &city[i][3]);
   }

   /* creates a distance matrix between every point */
   for(i = 0; i < 1000; i++)
   {
      for(j = 0; j < 1000; j++)
      {
         dist[i][j] = Distance(city[i], city[j]);
         if(dist[i][j] < min && i != j)
         {
            min = dist[i][j];
            i_ind = i;
            j_ind = j;
         }
      }
   }

   /* nearest neighbor algorithm */
   for(i = 0; i < 1000; i++)
   {
      if(dist[i_ind][i] < min1 && i != i_ind && i != j_ind)
      {
         min1 = dist[i_ind][i];
         ind1 = i;
      }
      if(dist[j_ind][i] < min2 && i != j_ind && i != i_ind)
      {
         min2 = dist[j_ind][i];
         ind2 = i; 
      }
   }

   if(min2 < min1)
   {
      order[0] = city[i_ind][0];
      order[1] = city[j_ind][0];
      order[2] = city[ind2][0];
      for(i = 0; i < 1000; i++)
      {
         dist[i][i_ind] = -1;
         dist[i][j_ind] = -1;
         dist[i_ind][i] = -1;
         dist[j_ind][i] = -1;
      }
   }
   else
   {
      order[0] = city[j_ind][0];
      order[1] = city[i_ind][0];
      order[2] = city[ind2][0];
      for(i = 0; i < 1000; i++)
      {    
         dist[i][i_ind] = -1;  /* values are set to -1 which means it has already been used */
         dist[i][j_ind] = -1;
         dist[i_ind][i] = -1;
         dist[j_ind][i] = -1;
      }
   }

   for(i = 3; i < 1000; i++)
   {
      min = 100000.0;
      for(j = 0; j < 1000; j++)
      {
         if(dist[ind2][j] < min && j != ind2 && dist[ind2][j] > 0)
         {
            min = dist[ind2][j];
            ind1 = j;
         }
      }
      order[i] = city[ind1][0];
      for(j = 0; j < 1000; j++)
      {
         dist[ind2][j] = -1.0;
         dist[j][ind2] = -1.0;
      }
      ind2 = ind1;
   }
   /* end of nearest neighbor algorithm */

   sum = totalDistance(order, city);
   bests = sum;
   eTest(order);
   arrayCopy(order, best);

   /* switch tests */
      for(i = 0; i < 1000; i++)
      {
         for(j = 0; j < 1000; j++)
         {
            tmp = order[i];
            order[i] = order[j];
            order[j] = tmp;
            sum = totalDistance(order, city);
            if(sum < bests)
            {
               bests = sum;
               arrayCopy(order, best);
            }
            else
            {
               arrayCopy(best, order);
            } 
         }
         printf("%d\n", i);
      }   

   eTest(order);
   printSequence(order);
   printf("Sum = %lf\n", sum);


   for(i = 0; i < 1000; i++)
   {
      free(city[i]);
      free(dist[i]);
   }

 
   free(order);
   free(dist);
   free(city);
   fclose(file);
 
   return 0;
} /* end of main */ 


/* computes distance between two points */
double Distance(int *a, int *b)
{
   double dist;
   dist = (double)((a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2]) + (a[3]                          - b[3]) * (a[3] - b[3]));
   dist = sqrt(dist);
   return(dist);
} /* end Distance */


/* computes the total distance across the sequence */
double totalDistance(int *order, int **city)
{
   int min1, min2, i;
   double sum = 0;

   for(i = 0; i < 999; i++)
   {
      min1 = order[i];
      min2 = order[i+1];
      sum += Distance(city[min1 - 1], city[min2 - 1]);
   }
   
   return(sum);  
} /* end of totalDistance */


/* prints out the order of the sequence */
void printSequence(int *order)
{
   int i;
   
   printf("\n");
   printf("Sequence: \n %d %d %d", order[0], order[1], order[2]);
   for(i = 3; i < 1000; i++)
   {   
      if(i%10 == 0)
         printf("\n"); 
      printf(" %d", order[i]);
   }
   printf("\n");
}  /* end of printSeq */


/* Test to make sure no 2 elements are repeated */
void eTest(int *order)
{
   int i, j;

   for(i = 0; i < 1000; i++)
   {
      for(j = 0; j < 1000; j++)
      {
         if(i == j)
            continue;
         else
         {
            if(order[i] == order[j])
               printf("ERROR: Order %d and %d are the same", i, j);
         }
      }
   }
} /* end of eTest */


/* copies array */
void arrayCopy(int *order, int *best)
{
   int i;

   for(i = 0; i < 1000; i++)
      best[i] = order[i]; 

} /* end of arrayCopy */


double localDistance(int *order, int **city)
{

} /* end of localDistance */
