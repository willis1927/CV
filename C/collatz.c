#include <stdio.h>
#include <cs50.h>

int collatz (int);
int count = 0;

int main (void)
{

    int n = get_int("Enter number: ");
    printf("%i steps\n", collatz(n));

}

int collatz (int n)
{
        if (n == 1)
            {
                return count;
            }
        else if (n % 2 == 0)
            {
                collatz(n / 2);
                count++;
            }
        else
            {
                collatz(3 * n + 1);
                count++;
            }
        return count;
}