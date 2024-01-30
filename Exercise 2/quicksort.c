
/* ────────────────────────────────────────────────────────────────────────── *
 │                                                                            │
 │ This file is part of the exercises for the Lectures on                     │
 │   "Foundations of High Performance Computing"                              │
 │ given at                                                                   │
 │   Master in HPC and                                                        │
 │   Master in Data Science and Scientific Computing                          │
 │ @ SISSA, ICTP and University of Trieste                                    │
 │                                                                            │
 │ contact: luca.tornatore@inaf.it                                            │
 │                                                                            │
 │     This is free software; you can redistribute it and/or modify           │
 │     it under the terms of the GNU General Public License as published by   │
 │     the Free Software Foundation; either version 3 of the License, or      │
 │     (at your option) any later version.                                    │
 │     This code is distributed in the hope that it will be useful,           │
 │     but WITHOUT ANY WARRANTY; without even the implied warranty of         │
 │     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          │
 │     GNU General Public License for more details.                           │
 │                                                                            │
 │     You should have received a copy of the GNU General Public License      │
 │     along with this program.  If not, see <http://www.gnu.org/licenses/>   │
 │                                                                            │
 * ────────────────────────────────────────────────────────────────────────── */


#if defined(__STDC__)
#  if (__STDC_VERSION__ >= 199901L)
#     define _XOPEN_SOURCE 700
#  endif
#endif
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <omp.h>
#include <mpi.h>
#include <time.h>
#include <stddef.h>


// ================================================================
//  MACROS and DATATYPES
// ================================================================


#if defined(_OPENMP)

// measure the wall-clock time
#define CPU_TIME (clock_gettime( CLOCK_REALTIME, &ts ), (double)ts.tv_sec + \
                  (double)ts.tv_nsec * 1e-9)

// measure the cpu thread time
#define CPU_TIME_th (clock_gettime( CLOCK_THREAD_CPUTIME_ID, &myts ), (double)myts.tv_sec +     \
                     (double)myts.tv_nsec * 1e-9)

#else

// measure ther cpu process time
#define CPU_TIME (clock_gettime( CLOCK_PROCESS_CPUTIME_ID, &ts ), (double)ts.tv_sec + \
                  (double)ts.tv_nsec * 1e-9)
#endif


#if defined(DEBUG)
#define VERBOSE
#endif

#if defined(VERBOSE)
#define PRINTF(...) printf(__VA_ARGS__)
#else
#define PRINTF(...)
#endif

//
// The data to be sorted consists in a structure, just to mimic that you
// may have to sort not basic types, whch may have some effects on the memory efficiency.
// The structure, defined below as data_t is just an array of DATA_SIZE double,
// where DATA_SDIZE is defined here below.
// However, for the sake of simplicity, we assume that we sort with respect one of
// the double in each structure, the HOTst one, where HOT is defined below (my
// choice was to set HOT to 0, so the code will use the first double to sort the
// data).
//
// Note that you can chnage the data structure and the ordering as you like.

#if !defined(DATA_SIZE)
#define DATA_SIZE 8
#endif
#define HOT       0

// let's define the default amount of data
//
#if (!defined(DEBUG) || defined(_OPENMP))
#define N_dflt    10000000
#else
#define N_dflt    10000
#endif


// let's define the data_t type
//
typedef struct
{
  double data[DATA_SIZE];
} data_t;

MPI_Datatype create_data_datatype() {
  MPI_Datatype data_datatype;

  data_t data_t_dummy;
  MPI_Aint displacements[1];
  MPI_Aint base_address;

  MPI_Get_address(&data_t_dummy, &base_address);
  MPI_Get_address(&data_t_dummy.data, &displacements[0]);

  displacements[0] = MPI_Aint_diff(displacements[0], base_address);

  int lengths[1] = {DATA_SIZE};
  MPI_Datatype types[1] = {MPI_DOUBLE};

  // Create a new MPI datatype
  MPI_Type_create_struct(1, lengths, displacements, types, &data_datatype);
  MPI_Type_commit(&data_datatype);

  return data_datatype;
}

// let's defined convenient macros for max and min between
// two data_t objects
//
#define MAX( a, b ) ( (a)->data[HOT] >(b)->data[HOT]? (a) : (b) );
#define MIN( a, b ) ( (a)->data[HOT] <(b)->data[HOT]? (a) : (b) );


// ================================================================
//  PROTOTYPES
// ================================================================

// let'ìs define the compare funciton that will be used by the
// sorting routine
//
typedef int (compare_t)(const void*, const void*);

// let's define the verifying function type, used to test the
// results
//
typedef int (verify_t)(data_t *, int, int, int);


// declare the functions
//
extern inline compare_t compare;        // the compare function
extern inline compare_t compare_ge;     // the compare for "greater or equal"
verify_t  verify_partitioning;          // verification functions
verify_t  verify_sorting;
verify_t  show_array;

// declare the partitioning function
//
extern inline int partitioning( data_t *, int, int, compare_t );

// declare the sorting function
//
void quicksort( data_t *, int, int, compare_t ); 
void openmp_quicksort(data_t**);
void MPI_quicksort(data_t**, int, int);

void merge(data_t*, data_t*, data_t*, size_t, size_t, compare_t);

// ================================================================
//  CODE
// ================================================================


int main ( int argc, char **argv )
{
  int rank, size;
  // ---------------------------------------------
  //  get the arguments
  //


  int N          = N_dflt;
  
  /* check command-line arguments */
  {
    int a = 0;
    
    if ( argc > ++a ) N = atoi(*(argv+a));
  }
  
  // ---------------------------------------------
  //  generate the array
  //
  
  data_t *data = (data_t*)malloc(N*sizeof(data_t));
  long int seed;

  #if defined(_OPENMP)
  #pragma omp parallel
  {
    int me             = omp_get_thread_num();
    short int seed     = time(NULL) % ( (1 << sizeof(short int))-1 );
    short int seeds[3] = {seed-me, seed+me, seed+me*2};

    #pragma omp for
      for ( int i = 0; i < N; i++ )
        data[i].data[HOT] = erand48( seeds );
  }
  #else
  {
    seed = time(NULL);
    srand48(seed);
    
    PRINTF("ssed is % ld\n", seed);
    
    for ( int i = 0; i < N; i++ )
      data[i].data[HOT] = drand48();
  }
  #endif

  
  // ---------------------------------------------
  //  process 
  //
  struct timespec ts;
  int    nthreads = atoi(getenv("OMP_NUM_THREADS"));
  double tstart = CPU_TIME;

  MPI_Init(&argc, &argv);

  MPI_Comm_rank(MPI_COMM_WORLD, &rank); // get current process id
  MPI_Comm_size(MPI_COMM_WORLD, &size); // get number of processes

  if (size == 1){
    #if defined(_OPENMP)
      
      openmp_quicksort(&data);

    #else

      quicksort( data, 0, N, compare_ge );

    #endif
  } else {
    MPI_quicksort(&data, size, rank);
  }

  double tend = CPU_TIME;  

  // ---------------------------------------------
  //  release the memory and stop
  //

  if ( verify_sorting( data, 0, N, 0) )
    printf("%d\t%g sec\n", nthreads, tend-tstart);
  else
    printf("the array is not sorted correctly\n");

  free( data );
  MPI_Finalize();

  return 0;

}


 #define SWAP(A,B,SIZE) do {int sz = (SIZE); char *a = (A); char *b = (B); \
    do { char _temp = *a;*a++ = *b;*b++ = _temp;} while (--sz);} while (0)

inline int partitioning( data_t *data, int start, int end, compare_t cmp_ge )
{
  
  // pick up the median of [0], [mid] and [end] as pivot
  //
  
  /* to be done */

  // pick up the last element as pivot
  //
  --end;  
  void *pivot = (void*)&data[end];

  // partition around the pivot element
  
  int pointbreak = end-1;
  for ( int i = start; i <= pointbreak; i++ )
    if( cmp_ge( (void*)&data[i], pivot ) )
      {
        while( (pointbreak > i) && cmp_ge( (void*)&data[pointbreak], pivot ) ) pointbreak--;
          if (pointbreak > i ) 
	          SWAP( (void*)&data[i], (void*)&data[pointbreak--], sizeof(data_t) );
      }  

  pointbreak += !cmp_ge( (void*)&data[pointbreak], pivot ) ;
  SWAP( (void*)&data[pointbreak], pivot, sizeof(data_t) );

  return pointbreak;
}


void quicksort( data_t *data, int start, int end, compare_t cmp_ge )
{

 #if defined(DEBUG)
 #define CHECK {							\
    if ( verify_partitioning( data, start, end, mid ) ) {		\
      printf( "partitioning is wrong\n");				\
      printf("%4d, %4d (%4d, %g) -> %4d, %4d  +  %4d, %4d\n",		\
	     start, end, mid, data[mid].data[HOT],start, mid, mid+1, end); \
      show_array( data, start, end, 0 ); }}
 #else
 #define CHECK
 #endif

  int size = end-start;
  if ( size > 2 )
    {
      int mid = partitioning( data, start, end, cmp_ge );

      CHECK;
      
      #if defined(_OPENMP_)
      #pragma omp parallel num_threads(2)
      {
        #pragma omp single nowait
        {
          quicksort( data, start, mid, cmp_ge );    // sort the left half
        }
        #pragma omp single nowait
        {
          quicksort( data, mid+1, end , cmp_ge );   // sort the right half
        }
      }
      #else
          quicksort( data, start, mid, cmp_ge );    // sort the left half
          quicksort( data, mid+1, end , cmp_ge );   // sort the right half
      #endif
    }
  else
    {
      if ( (size == 2) && cmp_ge ( (void*)&data[start], (void*)&data[end-1] ) )
	SWAP( (void*)&data[start], (void*)&data[end-1], sizeof(data_t) );
    }
}

#if defined(_OPENMP)
void openmp_quicksort(data_t** data){
  int size;
  int N = N_dflt;
  // Get the amount of threads
  #pragma omp parallel
  {
    #pragma omp master
    {

      size = omp_get_num_threads();

    }

  }

  // Calculate the workload for each thread

  int chunk_size = N / size; 
  data_t* final = (*data);
  // Sort the chunks in parallel
  #pragma omp parallel for 
    for (int i = 0; i < size; i++){
      int offset_i  = (i     < N%size) ? i   : N%size;
      int offset_i2 = ((i+1) < N%size) ? i+1 : N%size;

      quicksort( final, chunk_size*i + offset_i, chunk_size*(i+1) + offset_i2, compare_ge );
    
    }

  // Merge the chunks in into the final array ordered
  data_t* tmp;
  for (int i=1; i < size; i++){
    int offset_i  = (i     < N%size) ? i   : N%size;
    int offset_i2 = ((i+1) < N%size) ? i+1 : N%size;
    int more      = (i+1) <= N%size;
    tmp           = (data_t*)malloc((chunk_size*(i+1)+offset_i2)*sizeof(data_t));

    merge(final, (*data)+chunk_size*i+offset_i, tmp, chunk_size*i + offset_i, chunk_size + more, compare_ge);

    final = tmp;
  }

  *data = final;
}
#endif

void MPI_quicksort(data_t** data, int size, int rank){
  int N = N_dflt;

  // Defining the chunk size and allocate the memory for the chunk
  int chunk_size = N / size;
  int more = (N%size == 0) ? 0 : rank < N%size;

  data_t* chunk  = (data_t*)malloc((chunk_size + more) * sizeof(data_t));

  // Scatter the chunks to the processes
  if (rank == 0){
    chunk = memcpy(chunk, *data, (chunk_size + more) * sizeof(data_t));
    for (int i=1; i < size; i++){
      int offset_i  = (i    < N%size) ? i   : N%size;
      int offset_i2 = (i+1  < N%size) ? i+1 : N%size;
      int more_i    = i < N%size;

      MPI_Send((*data)+chunk_size*i + offset_i, chunk_size + more_i, create_data_datatype(), i, 0, MPI_COMM_WORLD);      
    }
  } else {
    MPI_Status status;

    MPI_Recv(chunk, chunk_size + more, create_data_datatype(), 0, 0, MPI_COMM_WORLD, &status);
  }

  // MPI_Scatter(*data, chunk_size, create_data_datatype(), chunk,
              // chunk_size, create_data_datatype(), 0, MPI_COMM_WORLD);

  // Sort the chunks
  quicksort( chunk, 0, chunk_size + more, compare_ge );

  // Gather the chunks to the root process
  data_t* final = chunk;
  if (rank == 0){
    MPI_Status status;
    data_t* tmp;
    data_t* recv;
    for (int i=1; i < size; i++){
      int offset_i  = ((i)   < N%size) ? i   : N%size;
      int offset_i2 = ((i+1) < N%size) ? i+1 : N%size;
      int more_i    = i < N%size;

      recv = (data_t*)malloc((chunk_size+more_i)*sizeof(data_t));
  
      // Retrive the data from the processes i
      MPI_Recv(recv, chunk_size+more_i, create_data_datatype(), i, 0, MPI_COMM_WORLD, &status);

      // Merge the previous chunks to the new one ordered
      tmp = (data_t*)malloc((chunk_size*(i+1) + offset_i2)*sizeof(data_t));
      merge(final, recv, tmp, chunk_size*i + offset_i, chunk_size + more_i, compare_ge);

      // Update the final chunk
      final = tmp;
    }
  
  free( recv );

  // If the process is not the root send the chunk to the root and finalize
  } else {
    MPI_Send(chunk, chunk_size + more, create_data_datatype(), 0, 0, MPI_COMM_WORLD);
    free( chunk );
    MPI_Finalize();
    
    exit(0);
  }

  // Free the memory allocated for the chunks
  free( chunk );

  *data = final;
}




 
int verify_sorting( data_t *data, int start, int end, int not_used )
{
  int i = start;
  while( (++i < end) && (data[i].data[HOT] >= data[i-1].data[HOT]) );
  return ( i == end );
}

int verify_partitioning( data_t *data, int start, int end, int mid )
{
  int failure = 0;
  int fail = 0;
  
  for( int i = start; i < mid; i++ )
    if ( compare( (void*)&data[i], (void*)&data[mid] ) >= 0 )
      fail++;

  failure += fail;
  if ( fail )
    { 
      printf("failure in first half\n");
      fail = 0;
    }

  for( int i = mid+1; i < end; i++ )
    if ( compare( (void*)&data[i], (void*)&data[mid] ) < 0 )
      fail++;

  failure += fail;
  if ( fail )
    printf("failure in second half\n");

  return failure;
}


void merge(data_t* arr1, data_t* arr2, data_t* arr3, size_t n1, size_t n2, compare_t cmp_ge){
    int i=0, j=0, k=0;

    while (i < n1 && j < n2) {
        if (arr1[i].data[HOT] < arr2[j].data[HOT]){
            arr3[k].data[HOT] = arr1[i].data[HOT];
            i++;
        } else {
            arr3[k].data[HOT] = arr2[j].data[HOT];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr3[k].data[HOT] = arr1[i].data[HOT];
        i++;
        k++;
    }

    while (j < n2) {
        arr3[k].data[HOT] = arr2[j].data[HOT];
        j++;
        k++;
    }
}

int show_array( data_t *data, int start, int end, int not_used )
{
  printf("[ ");
  for ( int i = start; i < end; i++ )
    printf( "%f ", data[i].data[HOT] );
  printf("] %d\n", not_used);
  return 0;
}


inline int compare( const void *A, const void *B )
{
  data_t *a = (data_t*)A;
  data_t *b = (data_t*)B;

  double diff = a->data[HOT] - b->data[HOT];
  return ( (diff > 0) - (diff < 0) );
}

inline int compare_ge( const void *A, const void *B )
{
  data_t *a = (data_t*)A;
  data_t *b = (data_t*)B;

  return (a->data[HOT] >= b->data[HOT]);
}
