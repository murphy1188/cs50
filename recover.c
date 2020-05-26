#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image");
        return 1;
    }
    BYTE buffer[512];
    int image_counter = 0;
    char *filename = malloc(8);
    FILE *image;

    
    FILE *fp = fopen(argv[1], "r");

    while (fread(&buffer, sizeof(BYTE), 512, fp) == 512)
    {
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            if (image_counter == 0)
            {
                sprintf(filename, "%03i.jpg", image_counter);
                image = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, image);
                image_counter++;
            }
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
            fwrite(&buffer, sizeof(BYTE), 512, image);
        }
    }
    return 0;
    free(buffer);



}
