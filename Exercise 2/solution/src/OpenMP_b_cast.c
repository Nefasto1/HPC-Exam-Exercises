#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// Initialize the buffer as threadprivate
int* buffer;
#pragma omp threadprivate( buffer )

int main(int argc, char** argv) {
    // A parameter needed (Number of elements in the array)
    if (argc < 2){
        printf("Insert the number of int to send\n");
        return 1;
    }

    // Get the number of elements
    int n = atoi(argv[1]);

    // Initialize the root's elements in the buffer
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

    // Broadcast the buffer between the threads
    #pragma omp parallel copyin(buffer)
    {
        int rank = omp_get_thread_num();
        int* private_array = (int*)malloc(n*sizeof(int));

        // Do a deep copy, we have propagated the pointer to the buffer
        for (int i=0; i < n; i++){
            private_array[i] = buffer[i];
        }

        // Print the results
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
        }
    }

    return 0;
}
