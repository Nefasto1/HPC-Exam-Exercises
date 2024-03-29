import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Open the dataframes
df_mpi  = pd.read_csv(f"results/quicksort_MPI.txt", sep="\t")
df_open = pd.read_csv(f"results/quicksort_openmp.txt", sep="\t")
df_seri = pd.read_csv(f"results/quicksort_serial.txt", sep="\t")

# Plot the Algorithms' Latency in function of the number of processors
for n in df_open["np"].unique():
    # Take the row where the number of processors is equal to n
    tmp_mpi       = df_mpi[df_mpi["np"] == n]
    tmp_open      = df_open[df_open["np"] == n]
    
    # Plot the curves
    plt.cla()
    plt.plot(np.log2(tmp_mpi ["Size"].unique()), tmp_mpi["Latency (ns)"]/1000, label="MPI")
    plt.plot(np.log2(tmp_open["Size"].unique()), tmp_open["Latency (ns)"]/1000, label="OpenMP")
    plt.plot(np.log2(df_seri["Size"].unique()), df_seri["Latency (ns)"]/1000, label="Serial")

    # Set the plot's informations
    plt.title(f"np:{n}")  
    plt.xlabel("log Size")
    plt.ylabel("Time (us)")
    
    # Set additional informations
    plt.xticks(np.log2(tmp_open["Size"].unique()))
    plt.grid()
    plt.legend()
    
    # Save the plots
    plt.savefig(f"inverted_plots/np:{n}.png")
