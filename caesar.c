#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // test if user entered key in command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // convert command line argument input for key to integer
    int key = atoi(argv[1]);
    
    // test if user entered valid key (integer greater than 0)
    if (key <= 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if ( isdigit(argv[1][i]) )
        {
        }
        else
        {
        printf("Usage: ./caesar key\n");
        return 1;
        }
    }
    
    // prompt user to input plaintext
    string s = get_string("plaintext: ");
    
    // convert plaintext to ciphertext
    printf("ciphertext: ");
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // convert uppercase plaintext letters to uppercase ciphertext letters
        if ( isupper(s[i]))
        {
            int alphaindexu = ((s[i] - 65 + key) % 26) + 65;
            printf("%c", alphaindexu);
        }
        // convert lowercase plain text letters to lowercase ciphertext letters
        else if ( islower(s[i]))
        {
            int alphaindexl = ((s[i] - 97 + key) % 26) + 97;
            printf("%c", alphaindexl);
        }
        // print spaces from plaintext input to ciphertext output
        else if ( isspace(s[i]))
        {
            printf(" ");
        }
        // print punction from plaintext input to ciphertext output
        else if ( ispunct(s[i]))
        {
            printf("%c", s[i]);
        }
    }
    printf("\n");
    return 0;
}