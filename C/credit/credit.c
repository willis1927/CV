#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card;
    do
    {
        card = get_long("Enter card number: ");
    }
    while (card < 0);

    int length = 0;
    int mod = 0;
    long trunc = card;
    bool even = false;
    int even_sum = 0;
    int odd_sum = 0;
    int check = 1;

    for (long i = 0; i < card; i = card - trunc)
    {
        mod = trunc % 10;
        trunc = trunc / 10;
        length++;

        if (length % 2 == 0)
        {
            int temp_mod = mod * 2;
            if (temp_mod > 9)
            {

                even_sum = even_sum + (temp_mod % 10);
                temp_mod = temp_mod / 10;
                even_sum = even_sum + (temp_mod % 10);
            }
            else
            {
                even_sum = even_sum + temp_mod;
            }
        }
        else
        {
            odd_sum = odd_sum + mod;
        }
    }

    check = (odd_sum + even_sum) % 10;

    if (check != 0)
    {
        printf("INVALID\n");
    }
    else if (length == 13 && mod == 4)
    {
        printf("VISA\n");
    }
    else if (length == 16 && mod == 4)
    {
        printf("VISA\n");
    }
    else if (length == 16)
    {
        mod = card / (10e13);
        printf("%i\n", mod);
        if (mod > 50 && mod < 56)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (length == 15)
    {
        mod = card / (10e12);
        if (mod == 34 || mod == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}