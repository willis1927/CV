#include "helpers.h"
#include <math.h>
#include <stdio.h>
void swap(RGBTRIPLE *a, RGBTRIPLE *b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int average = round((image[h][w].rgbtBlue + image[h][w].rgbtGreen + image[h][w].rgbtRed) / 3.0);
            image[h][w].rgbtBlue = average;
            image[h][w].rgbtGreen = average;
            image[h][w].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int k = width - 1;
        for (int j = 0; j < width / 2; j++)
        {
            swap(&image[i][j], &image[i][k]);
            k--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j].rgbtBlue = image[i][j].rgbtBlue;
            temp[i][j].rgbtGreen = image[i][j].rgbtGreen;
            temp[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            float avgB, avgG, avgR;
            avgB = 0;
            avgG = 0;
            avgR = 0;

            for (int k = (i - 1); k < (i + 2); k++)
            {
                for (int l = (j - 1); l < (j + 2); l++)
                {
                    if (l >= 0 && l < width && k >= 0 && k < height)
                    {
                        avgB += temp[k][l].rgbtBlue;
                        avgG += temp[k][l].rgbtGreen;
                        avgR += temp[k][l].rgbtRed;
                        count++;
                    }
                }
            }
            image[i][j].rgbtBlue = round(avgB / count);
            image[i][j].rgbtGreen = round(avgG / count);
            image[i][j].rgbtRed = round(avgR / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int xMatrix[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int yMatrix[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    RGBTRIPLE Gx[height][width];
    RGBTRIPLE Gy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            Gx[i][j].rgbtBlue = image[i][j].rgbtBlue;
            Gx[i][j].rgbtGreen = image[i][j].rgbtGreen;
            Gx[i][j].rgbtRed = image[i][j].rgbtRed;

            Gy[i][j].rgbtBlue = image[i][j].rgbtBlue;
            Gy[i][j].rgbtGreen = image[i][j].rgbtGreen;
            Gy[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int xtempB, xtempG, xtempR, ytempB, ytempG, ytempR, x, y;
            xtempB = xtempG = xtempR = ytempB = ytempG = ytempR = x = y = 0;

            for (int k = (i - 1); k < (i + 2); k++)
            {
                for (int l = (j - 1); l < (j + 2); l++)
                {
                    if (l >= 0 && l < width && k >= 0 && k < height)
                    {

                        xtempB += (Gx[k][l].rgbtBlue * xMatrix[y][x]);
                        xtempG += (Gx[k][l].rgbtGreen * xMatrix[y][x]);
                        xtempR += (Gx[k][l].rgbtRed * xMatrix[y][x]);

                        ytempB += (Gx[k][l].rgbtBlue * yMatrix[y][x]);
                        ytempG += (Gx[k][l].rgbtGreen * yMatrix[y][x]);
                        ytempR += (Gx[k][l].rgbtRed * yMatrix[y][x]);

                        x++;
                    }
                    else
                    {
                        x++;
                    }
                }
                y++;
                x = 0;
            }
            y = 0;
            int B = round(sqrt((xtempB * xtempB) + (ytempB * ytempB)));
            int G = round(sqrt((xtempG * xtempG) + (ytempG * ytempG)));
            int R = round(sqrt((xtempR * xtempR) + (ytempR * ytempR)));
            image[i][j].rgbtBlue = (B > 255) ? 255 : B;
            image[i][j].rgbtGreen = (G > 255) ? 255 : G;
            image[i][j].rgbtRed = (R > 255) ? 255 : R;
        }
    }
    return;
}
void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE temp = *a;
    *a = *b;

    *b = temp;
}
