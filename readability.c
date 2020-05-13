#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;
    // Prompt user to input reading sample to test
    
    string s = get_string("Text: ");
    
    // Get counts of letters, words, and sentences from user input
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if ((s[i] >= 'a' && s[i] <= 'z') || (s[i] >= 'A' && s[i] <= 'Z'))
        {
            letters++;
        }
        else if (s[i] == ' ')
        {
            words++;
        }
        else if (s[i] == '.' || s[i] == '!' || s [i] == '?')
        {
            sentences++;
        }
    }
    
    // Calculate avg number of letters per 100 words
    float l = 100 / (float) words * letters;
    
    // Calculate avg number of sentences per 100 words
    float x = 100 / (float) words * sentences;
    
    // Calculate Coleman-Liau index
    float index = round((0.0588 * l) - (0.296 * x) - 15.8);
    
    // Output reading level 
    if (index > 0 && index < 17)
    {
        printf("Grade %.0f\n", index);
    }
    else if (index >= 17)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }
}