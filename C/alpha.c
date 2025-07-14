#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main (void)
{
    string word = get_string("Enter word - ");
    int length = strlen(word);
    string test;
 for (int i = 0; i < length-1; i++)
 {
    if (word[i]<cword[i+1])
        {
            test = "Yes";
        }
        else
        {
            test = "No";
            i = length;
        }
 }
 printf("%s\n", test);
}