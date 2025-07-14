#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int current;
    int target;
    int years = 0;
    // Prompt for number of llamas
    do
    {
        current = get_int("How many llamas do you you have? ");
    }
    while (current < 9);

    // prompt for target number of llamas
    do
    {
        target = get_int("How many llamas would you like? ");
    }
    while (target < current);

    // calcuate number of years, each year 1/3 of current are born, 1/4 pass away
    while (current < target)
    {
        current += (current / 3) - (current / 4);
        years++;
    }

    // return how many years will it take to get to the target?
    printf("Years: %i\n", years);
}