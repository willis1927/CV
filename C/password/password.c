// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    int length = strlen(password);
    bool upper = false;
    bool lower = false;
    bool number = false;
    bool symbol = false;

    for (int i = 0; i < length; i++)
    {   char x = password[i];

        if(islower(x) != 0)
                    {
                        lower = true;
                    }
        if(isupper(x) != 0)
                    {
                        upper = true;
                    }
        if(isdigit(x) != 0)
                    {
                        number = true;
                    }
        if(ispunct(x) != 0)
                    {
                        symbol = true;
                    }
    }

    if (lower == true && upper == true && number == true && symbol == true)
    {
    return true;
    }
    else
    {
        return false;
    }
}
