#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <string.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    if (argc < 2){
        printf("Insert the size of the buffer");
        return 1;
    }

    int n = atoi(argv[1]);

    int rank, size;
    int* buffer = (int*)malloc(n * sizeof(int));
    MPI_Status status;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // get current process id
    MPI_Comm_size(MPI_COMM_WORLD, &size); // get number of processes

    if (size < 2) {
        printf("Please run with two processes.\n");
        MPI_Abort(MPI_COMM_WORLD, EXIT_FAILURE);
    }

    if (rank == 0){
        for (int i=0; i < n; i++)
            buffer[i] = 3;

        for (int i = 1; i < size; i++){
            // (msg, amount, type, dest, tag, communicator)
            MPI_Send(buffer, n, MPI_INT, i, 0, MPI_COMM_WORLD);
        }
        // printf("Root has sent the message to all the processes\n");
    }
    else{
        MPI_Recv(buffer, n, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
        
        // printf("Process %d [", rank);
        // for (int i=0; i < n; i++) {
        //     if (i) printf(", ");
        //     printf("%d", buffer[i]);
        // }
        // printf("]\n");
    }

    // free( buffer );
}