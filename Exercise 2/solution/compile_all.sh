# Load the compiler
module load openMPI/4.1.5/gnu

# Compile the .c code
mpicc src/MPI_b_cast_flat.c -o bin/MPI_b_cast_flat.o
mpicc src/MPI_b_cast_chain.c -o bin/MPI_b_cast_chain.o
mpicc src/MPI_b_cast_binary.c -o bin/MPI_b_cast_binary.o
mpicc -qopenmp src/OpenMP_b_cast.c -o bin/OpenMP_b_cast.o

# Ex 2b
mpicc -qopenmp src/quicksort.c -o bin/quicksort.o
