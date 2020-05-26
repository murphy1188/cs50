#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // Check that command line argument entered correctly 
    if (argc != 2)
    {
        printf("Usage: ./recover image");
        return 1;
    }
    // Declare variables
    BYTE buffer[512];
    int image_counter = 0;
    char *filename = malloc(8);
    FILE *image;

    // Open file from command line argument
    FILE *fp = fopen(argv[1], "r");
    // Condition that runs as long as there are at 512 bytes to read from file
    // If less than 512 bytes, means we've reached end of file
    while (fread(&buffer, sizeof(BYTE), 512, fp) == 512)
    {
        // Check if first 4 bytes are start of new jpeg file
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            // If no jpeg files found yet
            if (image_counter == 0)
            {
                sprintf(filename, "%03i.jpg", image_counter);
                image = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, image);
                image_counter++;
            }
            // If at least 1 jpeg file already found, close last jpeg file and open new jpeg file
            else if (image_counter > 0)
            {
                fclose(image);
                sprintf(filename, "%03i.jpg", image_counter);
                image = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, image);
                image_counter++;
            }
        }
        else if (image_counter > 0)
        {
            // Continues writing to jpeg file until new jpeg file is found
            fwrite(&buffer, sizeof(BYTE), 512, image);
        }
    }
    return 0;
    free(buffer);



}
