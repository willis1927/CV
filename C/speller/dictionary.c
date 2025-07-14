// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
void freenode(node *n);
// TODO: Choose number of buckets in hash table
const unsigned int N = 26;
unsigned int dsize = 0;
// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    //create cursor
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp (cursor -> word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor -> next;
        }

    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    int result = 0;
    FILE *inptr = fopen(dictionary,"r");
     if (inptr == NULL)
        {
            printf("error opening file.\n");
            return false;
        }

    char buffer[LENGTH + 1];
    //FILE *outptr = fopen("OutDictionary.txt", "w+");
    while (fscanf(inptr, "%s", buffer) != EOF)
    {
    node *n = malloc(sizeof(node));
    if (n == NULL)
    {
        return false;
    }
    strcpy(n->word,buffer);
    int index = hash(buffer);
    //check if index in hash table is empty, if yes add with Null, if no add to linked list
    if (table[index] == NULL)
       {
         n -> next = NULL;
       }
      else
       {
         n -> next = table[index];
       }
    table[index] = n;
    dsize += 1;
    //fprintf(outptr, "%s - %i - %p - %p\n" , buffer, index,n->word, n->next);

    }

    fclose(inptr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
   return dsize;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            freenode(table[i]);
        }
    }
    return true;
}

void freenode(node *n)
{
    if(n->next != NULL)
    {
         freenode(n->next);
     }
     free(n);
}
