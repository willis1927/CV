#include <cs50.h>
#include <stdio.h>

bool prime(int number);

int main(void)
{
    int min;
    do
    {
        min = get_int("Minimum: ");
    }
    while (min < 1);

    int max;
    do
    {
        max = get_int("Maximum: ");
    }
    while (min >= max);

    for (int i = min; i <= max; i++)
    {
        if (prime(i))
        {
            printf("%i\n", i);
        }
    }
}

bool prime(int number)
{
bool prime = false;

  if (number == 2)
    {
        prime = true;
    }
  for (int x = 2; x < number; x++)
  {
        if (number % x == 0)
        {
            prime = false;
            x = number;
        }
         else
         {
            prime = true;
         }
    }
return prime;
}
