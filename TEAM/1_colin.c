#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#ifndef min
       #define min( a, b) (  ((a) < (b)) ? (a) : (b) )
#endif


int main(int argc, char *argv[])
{
   int i,j,k,l, s, se, mins = 100000000, minse = 10000000;
   int *arr, *bests, *bestse;
   float N = atof(argv[1]);

   void Score(int *arr, float N, int *s, int *se);

   arr = malloc(6*sizeof(int));
   assert(arr);
   bests = malloc(6*sizeof(int));
   assert(bests);
   bestse = malloc(6*sizeof(int));
   assert(bestse);
 
   arr[0] = 1;
   bests[0] = 1;
   bestse[0] = 1;
   arr[5] = 100;
   bests[5] = 100;
   bestse[5] = 100;

   for(i = 2; i < 10; i++)
   {
      for(j = i + 1; j < 20 ; j++)
      {
         for(k = j + 1; k < 40; k++)
         { 
            for(l = k + 1; l < 70; l++)
            {
               arr[1] = i;
               arr[2] = j;
               arr[3] = k;
               arr[4] = l;
               Score(arr, N, &s, &se);
               if(s < mins)
               {
                  mins = s;
                  bests[1] = arr[1];
                  bests[2] = arr[2];
                  bests[3] = arr[3];
                  bests[4] = arr[4];
               }
               if (se < minse)
               {
                  minse = se;
		  bestse[1] = arr[1];
		  bestse[2] = arr[2];
		  bestse[3] = arr[3];
		  bestse[4] = arr[4];
               }
            }
         }
      }
   }
   printf("1, %d, %d, %d, %d\n", bests[1], bests[2], 
					bests[3], bests[4]);
   printf("1, %d, %d, %d, %d", bestse[1], bestse[2], 
					bestse[3], bestse[4]);
   free(arr);
   free(bests);
   free(bestse);

   return 0;
} /* end of main */


void Score(int *D, float N, int *s, int *se)
{
   int i, j, mini;
   int T[200];
   int E[200];

   *s = 0; 
   *se = 0;

   for(i = 0; i < 200; i++)
   {
      T[i] = 100;
      E[i] = 100;
   }

   for(i = 1; i < 200; i++)
   {
      if(i == D[0] || i == D[1] || i == D[2] || i == D[3] || i == D[4] || i == D[5])
      {
         T[i] = 1;
         E[i] = 1;
         if(i == D[5])
         {
            T[i] = 0;
            E[i] = 0;
         }
      }
      else
      {
         mini = 100;
         for(j = 0; j < 6; j++)
         {
            if((i - D[j] > 0))
            {
               mini = min(T[i - D[j]] + 1, mini);
            }
         } 
         if(i > 100)
            mini = min(mini, T[i - 100]);
         T[i] = mini;
      }
   }
 
   for(i = 1; i < 200; i++)
   {
      if(i == D[0] || i == D[1] || i == D[2] || i == D[3] || i == D[4] || i == D[5])
         continue;
      for(j = i + 1; j < 199; j++)
         E[i] =  min(E[i], T[j] + T[j - i]);
      E[i] = min(E[i], T[200 - i]);
   }
 
   for(i = 1; i < 100; i++)
   {
      if(i % 5 != 0){
         *s += T[i];
         *se += E[i];
      }
      else{
         *s += N * T[i];
         *se += N * E[i];
     }
   }

}  /* end of score */



