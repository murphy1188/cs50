#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int coins = 0;
    int q;
    int d;
    int n;
    int p;
    
    float dollars;
    do
    {
        dollars = get_float("How much change is owed? ");
    }
    while (dollars < 0);
    int cents = round(dollars * 100);
    
    for (q = 1; cents >= 25; q++)
    {
        cents -= 25;
        coins += 1;
    }
    for (d = 1; cents >= 10; d++)
    {
        cents -= 10;
        coins += 1;
    }
    for (n = 1; cents >= 5; n++)
    {
        cents -= 5;
        coins += 1;
    }
    for (p = 1; cents >= 1; p++)
    {
        cents -= 1;
        coins += 1;
    }
    printf("%i\n", coins);

}