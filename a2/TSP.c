#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

int main(int argc, char *argv[])
{
   FILE *file, *data, *result;
   int **city, *order;
   int i, j, k, tmp, i_ind, j_ind, flag, before, after;
   double min, sum;
   double **dist;
   double Distance(int *a, int *b);
   double totalDistance(int *order, double **dist);

   min = 1000000000.0;
   sum = 0.0;

   order = malloc(1000 * sizeof(int));
   assert(order);
   city = malloc(1000 * sizeof(int*));
   assert(city);
   dist = malloc(1000 * sizeof(double*));
   assert(dist);
   file = fopen(argv[1], "r");
   assert(file);
   data = fopen("data.dat", "r");
   assert(data);
   result = fopen("result.dat", "w");
   assert(result);

   /* fill in city array from file */
   for(i = 0; i < 1000; i++)
   {
      city[i] = malloc(4 * sizeof(int));
      assert(city[i]);
      dist[i] = malloc(1000 * sizeof(double));
      assert(dist[i]);   
      fscanf(file, "%d %d %d %d", &city[i][0], &city[i][1], &city[i][2], &city[i][3]);
      fscanf(data, "%d", &order[i]);
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

   sum = totalDistance(order, dist);
   printf("Sum = %lf\n", sum);

   for(k = 0; k < 30; k++)
   {
      for(i = 0; i < 1000; i++)
      {
         for(j = 0; j < 1000; j++)
         {
            flag = 0;
            before = 0;
            before += i == 0   ? 0 : dist[order[i - 1]][order[i]];
            before += i == 999 ? 0 : dist[order[i]][order[i + 1]];
            before += j == 0   ? 0 : dist[order[j - 1]][order[j]];
            before += j == 999 ? 0 : dist[order[j]][order[j + 1]];

            tmp = order[i];
            order[i] = order[j];
            order[j] = tmp;

            after = 0;
            after += i == 0   ? 0 : dist[order[i - 1]][order[i]];
            after += i == 999 ? 0 : dist[order[i]][order[i + 1]];
            after += j == 0   ? 0 : dist[order[j - 1]][order[j]];
            after += j == 999 ? 0 : dist[order[j]][order[j + 1]];
/*
            if(after < before)
            {
               flag = 1;
               break;
            }
            else */
            if(after > before)
            {   
               tmp = order[i];
               order[i] = order[j];
               order[j] = tmp;
            }
         }
         if(flag)
            break;
      }   
   }

   sum = totalDistance(order, dist);
   printf("Sum = %lf\n", sum);
  
   for(i = 0; i < 1000; i++)
      fprintf(result, "%d ", order[i]);
   fprintf(result, ";");

 /*  printf("Sum = %lf\n", sum); */


   for(i = 0; i < 1000; i++)
   {
      free(city[i]);
      free(dist[i]);
   }

 
   free(order);
   free(dist);
   free(city);
   fclose(file);
   fclose(data);
 
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
double totalDistance(int *order, double **dist)
{
   int i;
   double sum = 0;

   for(i = 0; i < 999; i++)
   {
      sum += dist[order[i]][order[i + 1]];
   }
  
   return(sum);  
} /* end of totalDistance */



