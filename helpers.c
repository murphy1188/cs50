#include "helpers.h"
#include "math.h"
#include "stdlib.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
           int avg = nearbyint(((float)image[i][j].rgbtRed + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtBlue) / 3);
           image[i][j].rgbtRed = avg;
           image[i][j].rgbtGreen = avg;
           image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int ogred = image[i][j].rgbtRed;
            int oggreen = image[i][j].rgbtGreen;
            int ogblue = image [i][j].rgbtBlue;
        
            int sepred = round((.393 * ogred) + (.769 * oggreen) + (.189 * ogblue));
            if (sepred > 255)
            {
               image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepred;
            }
            
            int sepgreen = round((.349 * ogred) + (.686 * oggreen) + (.168 * ogblue));
            if (sepgreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepgreen;
            }
            
            int sepblue = round((.272 * ogred) + (.534 * oggreen) + (.131 * ogblue));
            if (sepblue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepblue;
            }
        }
    }
    return;
}

// Reflect image horizontally

void swap(RGBTRIPLE *a, RGBTRIPLE *b);

void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {  
        for (int j = 0; j < width / 2; j++)
        {
            int revj = width - 1 - j;
            swap(&image[i][j], &image[i][revj]);

        }
    }
    return;
}

void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp = *a;
    *a = *b;
    *b = tmp;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE ogimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ogimage[i][j] = image[i][j];
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Blur pixels not on edges
            if ((i > 0 && (i < height - 1)) && (j > 0 && j < (width - 1)))
            {
                int avgRed = nearbyint(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + ogimage[i + 1][j].rgbtRed + ogimage[i + 1][j + 1].rgbtRed) / 9);
                int avgGreen = nearbyint(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen + ogimage[i + 1][j + 1].rgbtGreen) / 9);
                int avgBlue = nearbyint(((float)ogimage[i - 1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue + ogimage[i + 1][j + 1].rgbtBlue) / 9);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top row/0th row if not in corner
            else if (i == 0 && j > 0 && j < width)
            {
                int avgRed = nearbyint(((float)ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + ogimage[i + 1][j].rgbtRed + ogimage[i + 1][j + 1].rgbtRed) / 6);
                int avgGreen = nearbyint(((float)ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen + ogimage[i + 1][j + 1].rgbtGreen) / 6);
                int avgBlue = nearbyint(((float)ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue + ogimage[i + 1][j + 1].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in 0th column if not in corner
            else if (i > 0 && i < height && j == 0)
            {
                int avgRed = nearbyint(((float)ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed + ogimage[i + 1][j].rgbtRed + ogimage[i + 1][j + 1].rgbtRed) / 6);
                int avgGreen = nearbyint(((float)ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen + ogimage[i + 1][j + 1].rgbtGreen) / 6);
                int avgBlue = nearbyint(((float)ogimage[i -1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue + ogimage[i + 1][j + 1].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in bottom row (height - 1) if not in corner
            else if ((i == height - 1) && (j > 0 && (j < width - 1)))
            {
                int avgRed = nearbyint(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed) / 6);
                int avgGreen = nearbyint(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen) / 6);
                int avgBlue = nearbyint(((float)ogimage[i - 1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in last column (width - 1) if not in corner
            else if ((i > 0 && (i < height -1)) && (j == width - 1))
            {
                int avgRed = nearbyint(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + ogimage[i + 1][j].rgbtRed) / 6);
                int avgGreen = nearbyint(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen) / 6);
                int avgBlue = nearbyint(((float)ogimage[i -1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top left corner
            else if (i == 0 && j == 00)
            {
                int avgRed = nearbyint(((float)ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed + ogimage[i + 1][j].rgbtRed + ogimage[i + 1][j + 1].rgbtRed) / 4);
                int avgGreen = nearbyint(((float)ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen + ogimage[i + 1][j + 1].rgbtGreen) / 4);
                int avgBlue = nearbyint(((float)ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue + ogimage[i + 1][j + 1].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top right corner
            else if (i == 0 && j == width)
            {
                int avgRed = nearbyint(((float)ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + ogimage[i + 1][j].rgbtRed) / 4);
                int avgGreen = nearbyint(((float)ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen) / 4);
                int avgBlue = nearbyint(((float)ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in bottom left corner
            else if (i == height && j == 0)
            {
                int avgRed = nearbyint(((float)ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed) / 4);
                int avgGreen = nearbyint(((float)ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen) / 4);
                int avgBlue = nearbyint(((float)ogimage[i - 1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in bottom right corner
            else if (i == height && j == width)
            {
                int avgRed = nearbyint(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed) / 4);
                int avgGreen = nearbyint(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen) / 4);
                int avgBlue = nearbyint(((float)ogimage[i - 1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top right corner
            else if (i == 0 && j == width)
            {
                int avgRed = nearbyint(((float)ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + ogimage[i + 1][j].rgbtRed) / 4);
                int avgGreen = nearbyint(((float)ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen) / 4);
                int avgBlue = nearbyint(((float)ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;

            }
        }
    }
    return;
}
