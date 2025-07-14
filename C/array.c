#include <cs50.h>
#include <stdio.h>


int main(void)
{
   int length;

   do
   {
    length = get_int("Length: ");
   }
    while (length < 0);

    int array[length];

    array[0] = 1;

    for (int i = 0; i < length; i++)
    {
        array[1+i] = array[i]*2;
        printf("%i\n",array[i]);
    }

}