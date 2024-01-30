#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int buffer;
#pragma omp threadprivate( buffer )

int main(int argc, char** argv) {
    int size;
    int current=0;

    #pragma omp parallel
    {
        #pragma omp master
        {
            buffer = 3;
            size = omp_get_num_threads();
        }
    }

    printf("%d", size);
    #pragma omp barrier

    #pragma omp parallel copyin(buffer)
    {
        int rank = omp_get_thread_num();
        while current < size{
            if current == rank{
                
            }
        }
        printf("Process %d received the message from root correctly: %d\n", rank, buffer);
    }
}