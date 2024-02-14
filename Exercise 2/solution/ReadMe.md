# Exercise 2

To compile the codes we used the gnu or the icc compiler, or use the command:

```./compile_all.sh```

# Exercise 2a
To run these codes use the commands:

```mpirun -np <num> OpenMP_b_cast.o <size>```

```mpirun -np <num> MPI_b_cast_flat.o <size>```

```mpirun -np <num> MPI_b_cast_chain.o <size>```

```mpirun -np <num> MPI_b_cast_binary.o <size>```

where:
  - `<num>` is the number of processes to run, it must be one for OpenMP code and at least 2 for the MPI code.
  - `<library>` must be equal to "OpenMP" or "MPI" (this just identify the code you want to use)
  - `<size>` is the number of integer in the array which we want to propagate

# Work in Progress
## Exercise 2b
To create the binary files for the .c file execute the commands:

```mpicc [-qopenmp] quicksort.c -o quicksort.o```

where:
  - `[-qopenmp]` is the flag to add if we want to use also the OpenMP library 

To run this code use the commands:

```export OMP_NUM_THREADS=<n_threads>```

```mpirun -np <num> quicksort_openmp.o [size]```

where:
  - `<n_threads>` is the number of threads with which run the code
  - `<num>` is the number of processes with which run the code
  - `[size]` is the number of double in the array to sort (default 10000000)

To get the algorithms times we can run the slurm jobs with the commands:

```sbatch <.job file> <MaxProcs> <MaxNumInt> <Iteration>```

where:
  - `<.job file>` is one of in the repository
  - `<MaxProcs>` is the number of processes/threads to use
  - `<MaxNumInt>` is the number of integer (or double for quicksort) in the array used
  - `<Iteration>` is the number of iteration to execute

Then you can plot this results with running the python code.
