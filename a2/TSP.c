#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

int main()
{
   FILE *file;
   int **city, *order;
   int i, j, i_ind, j_ind, ind1, ind2, min1 = 1000000, min2 = 100000;
   double min, sum;
   double **dist;
   double Distance(int *a, int *b);

   min = 1000000000.0;
   sum = 0.0;

   order = malloc(1000 * sizeof(int));
   assert(order);
   city = malloc(1000 * sizeof(int*));
   assert(city);
   dist = malloc(1000 * sizeof(double*));
   assert(dist);
   file = fopen("travelingtest", "r");
   assert(file);

   for(i = 0; i < 1000; i++)
   {
      city[i] = malloc(4 * sizeof(int));
      assert(city[i]);
      dist[i] = malloc(1000 * sizeof(double));
      assert(dist[i]);   
      fscanf(file, "%d %d %d %d", &city[i][0], &city[i][1], &city[i][2], &city[i][3]);
   }

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
         dist[i][i_ind] = -1;
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

   for(i = 0; i < 999; i++)
   {
      min1 = order[i];
      min2 = order[i+1];
      sum += Distance(city[min1 - 1], city[min2 - 1]);
   }

   printf("\n");
   printf("Sequence: \n %d %d %d", order[0], order[1], order[2]);
   for(i = 3; i < 1000; i++)
   {   
      if(i%10 == 0)
         printf("\n"); 
      printf(" %d", order[i]);
   }
   printf("\n");
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
} 


double Distance(int *a, int *b)
{
   double dist;
   dist = (double)((a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2]) + (a[3]                          - b[3]) * (a[3] - b[3]));
   dist = sqrt(dist);
   return(dist);

}
