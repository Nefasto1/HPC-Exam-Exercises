# Load the compiler
module load openMPI/4.1.5/icc

# Compile the .c code
mpicc src/MPI_b_cast.c -o bin/MPI_b_cast.o
mpicc -qopenmp src/OpenMP_b_cast.c -o bin/OpenMP_b_cast.o
mpicc -qopenmp src/quicksort.c -o bin/quicksort.o
