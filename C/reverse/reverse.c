#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    char *infile = argv[1];

    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }
    // Open input file for reading
    // TODO #2

        FILE *inptr = fopen(infile,"r");
        if (inptr == NULL)
        {
            printf("error opening file%s.\n", infile);
            return 1;
        }

    // Read header
    // TODO #3
   WAVHEADER header;
   fread(&header, sizeof(WAVHEADER), 1, inptr);
   long int start = ftell(inptr);
   //printf("Start block is : %li\n", start);

        // Use check_format to ensure WAV format
    // TODO #4
    if (check_format(header) == 0)
    {
        printf("Not a Wave file");
    }

    // Open output file for writing
    // TODO #5
    char *outfile = argv[2];
    FILE *outptr = fopen(outfile, "wb");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 3;
    }
    // Write header to file
    // TODO #6
    fwrite(&header, sizeof(WAVHEADER), 1, outptr);
    // Use get_block_size to calculate size of block
    // TODO #7
    int size = get_block_size(header);

    // Write reversed audio to file
    // TODO #8
    BYTE buffer[size];
    for (fseek(inptr, 0 - size ,SEEK_END); ftell(inptr) >= start; fseek(inptr,0- (2 * size), SEEK_CUR))
    {
    fread(&buffer, size, 1, inptr);
    fwrite(&buffer, size, 1, outptr);
    }

    fclose(inptr);
    fclose(outptr);
}

int check_format(WAVHEADER header)
{
    // TODO #4
     if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
        {
            if (header.audioFormat == 1)
            {
            return 1;
            }
        }
        printf("false\n");
        return 0;
}



int get_block_size(WAVHEADER header)
{
    // TODO #7
    int block_size = header.numChannels * (header.bitsPerSample/8);
    //printf("Block Size : %i\n", block_size);
    return block_size;

}