#include <cs50.h>
#include <stdio.h>
#include <string.h>

int count_words(string text);
int count_letters(string text);
int count_sentances(string text);

int main(void)
{
    string text = get_string("Text: ");

    float letters = count_letters(text);
    float words = count_words(text);
    float sentances = count_sentances(text);
    float avg_let = letters / words * 100.0;
    float avg_sen = sentances / words * 100.0;
    float index = 0.0588 * avg_let - 0.296 * avg_sen - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index < 16)
    {
        printf("Grade %.0f\n", index);
    }
    else
    {
        printf("Grade 16+\n");
    }
}

int count_letters(string text)
{
    int count = 0;
    int length = strlen(text);

    for (int i = 0; i < length; i++)
    {
        if (text[i] > 64 && text[i] < 91)
        {
            count++;
        }
        else if (text[i] > 96 && text[i] < 123)
        {
            count++;
        }
    }

    return count;
}

int count_words(string text)
{
    int count = 1;
    int length = strlen(text);

    for (int i = 0; i < length; i++)
    {
        if (text[i] == 32)
        {
            count++;
        }
    }
    return count;
}

int count_sentances(string text)
{
    int count = 0;
    int length = strlen(text);

    for (int i = 0; i < length; i++)
    {
        if (text[i] == 63 || text[i] == 46 || text[i] == 33)
        {
            count++;
        }
    }
    return count;
}