#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <string.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    // Take in input the size of the buffer
    if (argc < 2){
        printf("Insert the size of the buffer");
        return 1;
    }

    // Obtain the size
    int n = atoi(argv[1]);

    // Initialize the buffer
    int rank, size;
    int* buffer = (int*)malloc(n * sizeof(int));
    MPI_Status status;

    // Get the number of processes and the process id
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
    MPI_Comm_size(MPI_COMM_WORLD, &size); 

    // Needed at least two processes
    if (size < 2) {
        printf("Please run with two processes.\n");
        MPI_Abort(MPI_COMM_WORLD, EXIT_FAILURE);
    }

    // If the root process
    if (rank == 0){
        // Initialize the buffer
        for (int i=0; i < n; i++)
            buffer[i] = 3;

        MPI_Send(buffer, n, MPI_INT, 1, 0, MPI_COMM_WORLD);
        // printf("Root has sent the message to all the processes\n");
    }
    // If non-root process
    else {
        // Obtain the data
        MPI_Recv(buffer, n, MPI_INT, rank-1, 0, MPI_COMM_WORLD, &status);
        
        // Print the results
        printf("Process %d [", rank);
        for (int i=0; i < n; i++) {
            if (i) printf(", ");
            printf("%d", buffer[i]);
        }
        printf("]\n");
        
        if (rank != size-1)
            MPI_Send(buffer, n, MPI_INT, rank+1, 0, MPI_COMM_WORLD);
    }

    free( buffer );
}
