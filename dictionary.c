// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Keeps track of word count as words are added to dictionary
int word_counter;



// Number of buckets in hash table
const unsigned int N = 100;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hash_code = hash(word);
    node *cursor = table[hash_code];
    while (cursor != NULL && strcasecmp(cursor->word, word) != 0)
        {
            cursor = cursor->next;
        }
    if (cursor == NULL)
    {
        return false;
    }
    return true;

    

}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;
    char c;
    for (int i = 0; word[i] != '\0'; i++)
    {
        c = tolower(word[i]);
        sum += c;
    }
    sum = sum % N;
    return sum;
}

void init_hash_table()
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    int index = 0;
    node *tmp = NULL;
    char dict_word[LENGTH];
    
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("File not opened\n");
        return false;
    }
    while (fscanf(dict, "%s", dict_word) == 1)
    {

                index = hash(dict_word);
                tmp = malloc(sizeof(node));
                strcpy(tmp->word, dict_word);
                tmp->next = table[index];
                table[index] = tmp;
                word_counter++;
    }
    if (word_counter == 0)
    {
        printf("No words found\n");
    }
   
    return true;
}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (word_counter > 0)
    {
        printf("%i words have been added\n", word_counter);
        return word_counter;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor;
    node *tmp;
    for (int i = 0; i < N; i++)
    {
        tmp = table[i];
        cursor = table[i];
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
        return true;
    }
    return false;
}

