#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int* buffer;
#pragma omp threadprivate( buffer )

int main(int argc, char** argv) {
    if (argc < 2){
        printf("Insert the number of int to send\n");
        return 1;
    }

    int n = atoi(argv[1]);

    #pragma omp parallel
    {
        #pragma omp master
        {
            buffer = calloc(n, sizeof(int));
            
            for(int i=0; i < n; i++){
                buffer[i] = 3;
            }
        }
    }
    #pragma omp barrier

    #pragma omp parallel copyin(buffer)
    {
        int rank = omp_get_thread_num();
        int* private_array = (int*)malloc(n*sizeof(int));

        for (int i=0; i < n; i++){
            private_array[i] = buffer[i];
        }

        /*
        #pragma omp critical
        {
            ("%p", buffer);
            printf("Process %d [", rank);
            for (int i=0; i < n; i++) {
                if (i) printf(", ");
                printf("%d", buffer[i]);
            }
            printf("]\n");
            printf("%d, %d, %p\n", rank, buffer, &buffer)
        } */
    }

    return 0;
}
