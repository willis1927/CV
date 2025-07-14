#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Enter pyramid height: ");
    }
    while (height < 1 || height > 9);
    for (int i = 0; i < height; i++)
    {
        for (int space = i; height - space > 1; space++)
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("  ");

        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}