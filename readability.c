#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;
    string s = get_string("Text: ");
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
    float l = 100 / (float) words * letters;
    float x = 100 / (float) words * sentences;
    float index = round((0.0588 * l) - (0.296 * x) - 15.8);
    
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