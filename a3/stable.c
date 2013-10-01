#include <stdio.h>
#include <stdlib.h>
#include <math.h>



int main()
{
   int pos, i, j;
   int t1, t2;


   for(i = -15; i < 16; i++)
   {
      for(j = 1; j < 13; j++)
      {
         t1 = -9;
         t2 = -3;
         if(i < -3)
            t1 += abs(i + 3) * abs(j);
         else
            t1 -= abs(i + 3) * abs(j);
         if(i < -1)
            t2 += abs(i + 1) * abs(j);
         else
            t2 -= abs(i + 1) * abs(j);
         if(t1 <= 0 && t2 >= 0)
            printf("Weight %d stable at pos %d\n", j, i);
      }
   }

   return(0);

}
