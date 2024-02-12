import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Open the dataframes
df_mpi       = pd.read_csv(f"results/b_cast_mpi.txt", sep="\t")
df_true      = pd.read_csv(f"results/b_cast_mpi_true.txt", sep="\t")
df_open      = pd.read_csv(f"results/b_cast_openmp.txt", sep="\t")

# Plot the Algorithms' Latency in function of the number of processors
for n in df_open["Size"].unique():
    # Take the row where the number of processors is equal to n
    tmp_mpi       = df_mpi[df_mpi["Size"] == n]
    tmp_true      = df_true[df_true["Size"] == n]
    tmp_open      = df_open[df_open["Size"] == n]
    
    # Plot the curves
    plt.cla()
    plt.plot(tmp_mpi ["np"].unique(), tmp_mpi["Latency (ns)"]/1000, label="MPI")
    plt.plot(tmp_true["np"].unique(), tmp_true["Latency (ns)"]/1000, label="MPI True")
    plt.plot(tmp_open["np"].unique(), tmp_open["Latency (ns)"]/1000, label="OpenMP")

    # Set the plot's informations
    plt.title(f"Size:{n}")  
    plt.xlabel("np")
    plt.ylabel("Time (us)")
    
    # Set additional informations
    plt.xticks(tmp_open["np"].unique())
    plt.grid()
    plt.legend()
    
    # Save the plots
    plt.savefig(f"plots/Size:{n}.png")
    