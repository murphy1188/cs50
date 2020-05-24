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
            // Calculate average of each value for each pixel
            int avg = nearbyint(((float)image[i][j].rgbtRed + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtBlue) / 3);
            // Apply average value to each color, red, green, and blue
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
            // Get original values for red, green, blue
            int ogred = image[i][j].rgbtRed;
            int oggreen = image[i][j].rgbtGreen;
            int ogblue = image [i][j].rgbtBlue;
        
            // Apply formula for sepia red to original red value
            int sepred = round((.393 * ogred) + (.769 * oggreen) + (.189 * ogblue));
            // Check that sepia red value is not more than 255
            if (sepred > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            // Assign sepia red to pixel
            else
            {
                image[i][j].rgbtRed = sepred;
            }
            // Apply formula for sepia green to original green value
            int sepgreen = round((.349 * ogred) + (.686 * oggreen) + (.168 * ogblue));
            // Check that sepia green value is not more than 255
            if (sepgreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            // Assign sepia green to pixel
            else
            {
                image[i][j].rgbtGreen = sepgreen;
            }
            // Apply for sepia blue to original blue value
            int sepblue = round((.272 * ogred) + (.534 * oggreen) + (.131 * ogblue));
            // Check that sepia blue value is not more than 255
            if (sepblue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            // Assign sepia blue to pixel
            else
            {
                image[i][j].rgbtBlue = sepblue;
            }
        }
    }
    return;
}

// Reflect image horizontally
// Swap function prototype
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
// Swap function to reverse pixel order in each row
void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp = *a;
    *a = *b;
    *b = tmp;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Make copy of original image
    RGBTRIPLE ogimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ogimage[i][j] = image[i][j];
        }
    }
    
    for (int i = 0; i <= height; i++)
    {
        for (int j = 0; j <= width; j++)
        {
            //Blur pixels not on edges
            if ((i > 0 && (i < height - 1)) && (j > 0 && j < (width - 1)))
            {
                int avgRed = round(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + 
                                    ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + 
                                    ogimage[i + 1][j].rgbtRed + ogimage[i + 1][j + 1].rgbtRed) / 9);
                int avgGreen = round(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + 
                                      ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + 
                                      ogimage[i + 1][j].rgbtGreen + ogimage[i + 1][j + 1].rgbtGreen) / 9);
                int avgBlue = round(((float)ogimage[i - 1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + 
                                     ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + 
                                     ogimage[i + 1][j].rgbtBlue + ogimage[i + 1][j + 1].rgbtBlue) / 9);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top row/0th row if not in corner
            if (i == 0 && j > 0 && j < width - 1)
            {
                int avgRed = round(((float)ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed + 
                                    ogimage[i + 1][j - 1].rgbtRed + ogimage[i + 1][j].rgbtRed + ogimage[i + 1][j + 1].rgbtRed) / 6);
                int avgGreen = round(((float)ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen + 
                                      ogimage[i + 1][j - 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen + ogimage[i + 1][j + 1].rgbtGreen) / 6);
                int avgBlue = round(((float)ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue + 
                                     ogimage[i + 1][j - 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue + ogimage[i + 1][j + 1].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in 0th column if not in corner
            if (i > 0 && i < height && j == 0)
            {
                int avgRed = round(((float)ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + ogimage[i][j].rgbtRed + 
                                    ogimage[i][j + 1].rgbtRed + ogimage[i + 1][j].rgbtRed + ogimage[i + 1][j + 1].rgbtRed) / 6);
                int avgGreen = round(((float)ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + ogimage[i][j].rgbtGreen + 
                                      ogimage[i][j + 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen + ogimage[i + 1][j + 1].rgbtGreen) / 6);
                int avgBlue = round(((float)ogimage[i - 1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + ogimage[i][j].rgbtBlue + 
                                     ogimage[i][j + 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue + ogimage[i + 1][j + 1].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in bottom row (height - 1) if not in corner
            if ((i == height - 1) && (j > 0 && (j < width - 1)))
            {
                int avgRed = round(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + 
                                    ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed) / 6);
                int avgGreen = round(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + 
                                      ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen) / 6);
                int avgBlue = round(((float)ogimage[i - 1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + 
                                     ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in last column (width - 1) if not in corner
            if ((i > 0 && (i < height)) && (j == width - 1))
            {
                int avgRed = round(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i][j - 1].rgbtRed + 
                                    ogimage[i][j].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + ogimage[i + 1][j].rgbtRed) / 6);
                int avgGreen = round(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i][j - 1].rgbtGreen + 
                                      ogimage[i][j].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen) / 6);
                int avgBlue = round(((float)ogimage[i - 1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i][j - 1].rgbtBlue + 
                                     ogimage[i][j].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue) / 6);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top left corner
            if (i == 0 && j == 00)
            {
                int avgRed = round(((float)ogimage[i][j].rgbtRed + ogimage[i][j + 1].rgbtRed + ogimage[i + 1][j].rgbtRed + 
                                    ogimage[i + 1][j + 1].rgbtRed) / 4);
                int avgGreen = round(((float)ogimage[i][j].rgbtGreen + ogimage[i][j + 1].rgbtGreen + ogimage[i + 1][j].rgbtGreen + 
                                      ogimage[i + 1][j + 1].rgbtGreen) / 4);
                int avgBlue = round(((float)ogimage[i][j].rgbtBlue + ogimage[i][j + 1].rgbtBlue + ogimage[i + 1][j].rgbtBlue + 
                                     ogimage[i + 1][j + 1].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top right corner
            if (i == 0 && (j == width - 1))
            {
                int avgRed = round(((float)ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + 
                                    ogimage[i + 1][j].rgbtRed) / 4);
                int avgGreen = round(((float)ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + 
                                      ogimage[i + 1][j].rgbtGreen) / 4);
                int avgBlue = round(((float)ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + 
                                     ogimage[i + 1][j].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in bottom left corner
            if ((i == height - 1) && j == 0)
            {
                int avgRed = round(((float)ogimage[i - 1][j].rgbtRed + ogimage[i - 1][j + 1].rgbtRed + ogimage[i][j].rgbtRed + 
                                    ogimage[i][j + 1].rgbtRed) / 4);
                int avgGreen = round(((float)ogimage[i - 1][j].rgbtGreen + ogimage[i - 1][j + 1].rgbtGreen + ogimage[i][j].rgbtGreen + 
                                      ogimage[i][j + 1].rgbtGreen) / 4);
                int avgBlue = round(((float)ogimage[i - 1][j].rgbtBlue + ogimage[i - 1][j + 1].rgbtBlue + ogimage[i][j].rgbtBlue + 
                                     ogimage[i][j + 1].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in bottom right corner
            if ((i == (height - 1)) && (j == (width - 1)))
            {
                int avgRed = round(((float)ogimage[i - 1][j - 1].rgbtRed + ogimage[i - 1][j].rgbtRed + ogimage[i][j - 1].rgbtRed + 
                                    ogimage[i][j].rgbtRed) / 4);
                int avgGreen = round(((float)ogimage[i - 1][j - 1].rgbtGreen + ogimage[i - 1][j].rgbtGreen + ogimage[i][j - 1].rgbtGreen + 
                                      ogimage[i][j].rgbtGreen) / 4);
                int avgBlue = round(((float)ogimage[i - 1][j - 1].rgbtBlue + ogimage[i - 1][j].rgbtBlue + ogimage[i][j - 1].rgbtBlue + 
                                     ogimage[i][j].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;
            }
            // Blur pixels in top right corner
            if (i == 0 && j == width - 1)
            {
                int avgRed = round(((float)ogimage[i][j - 1].rgbtRed + ogimage[i][j].rgbtRed + ogimage[i + 1][j - 1].rgbtRed + 
                                    ogimage[i + 1][j].rgbtRed) / 4);
                int avgGreen = round(((float)ogimage[i][j - 1].rgbtGreen + ogimage[i][j].rgbtGreen + ogimage[i + 1][j - 1].rgbtGreen + 
                                      ogimage[i + 1][j].rgbtGreen) / 4);
                int avgBlue = round(((float)ogimage[i][j - 1].rgbtBlue + ogimage[i][j].rgbtBlue + ogimage[i + 1][j - 1].rgbtBlue + 
                                     ogimage[i + 1][j].rgbtBlue) / 4);
                image[i][j].rgbtRed = avgRed;
                image[i][j].rgbtGreen = avgGreen;
                image[i][j].rgbtBlue = avgBlue;

            }
        }
    }
    return;
}
