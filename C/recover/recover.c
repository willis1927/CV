#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
 if (argc !=2)
 {
    printf("Usage: ./recover IMAGE\n");
    return 1;
 }

 FILE *file = fopen(argv[1],"r");
 int BYTE[4] = 0;

 while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
{
fread(buffer[0], sizeof(BYTE), 1, file);
}


    printf("\n");

    //= 0xff
    //= 0xd8
    //= 0xff
    //=(buffer[3] & 0xf0) == 0xe0
}