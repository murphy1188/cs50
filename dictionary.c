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
const unsigned int N = 2500;

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
{   // Used hash function from Doug LLoyd's CS50 video on hash tables, added tolower function
    // to conver all letters in each word to lowercase
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

// Initialize hash table
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
    
    // Open dictionary
    FILE *dict = fopen(dictionary, "r");
    // If file is NULL, returns false
    if (dict == NULL)
    {
        printf("File not opened\n");
        return false;
    }
    //Reads each word from dictionary file, inserts each word to hash table
    while (fscanf(dict, "%s", dict_word) == 1)
    {
        // Gets hash table index for each word from dictionary file
        index = hash(dict_word);
        // Allocates enough memory to create a node for each word being added to hash table 
        tmp = malloc(sizeof(node));
        // Copies each word from dictionary file into hash table
        strcpy(tmp->word, dict_word);
        // Changes pointer for added to word to head of the table index location
        tmp->next = table[index];
        // The added word is now at the head of the table index location
        table[index] = tmp;
        // Adds 1 to total word counter
        word_counter++;
    }
    if (word_counter == 0)
    {
        printf("No words found\n");
    }
    // Close dictionary file
    fclose(dict);
    return true;
}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (word_counter > 0)
    {
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
    for (int i = 0; i < N + 1; i++)
    {
        tmp = table[i];
        cursor = table[i];
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
        if (cursor == NULL)
        {
            free(tmp);
        }
    }
    return true;
}

