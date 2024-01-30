import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Open the dataframes
df_mpi       = pd.read_csv(f"results/prova_MPI.txt", sep="\t")
df_true      = pd.read_csv(f"results/prova_MPI_true.txt", sep="\t")
df_open      = pd.read_csv(f"results/prova_OpenMP.txt", sep="\t")

# Plot the Algorithms' Latency in function of the number of processors
for n in df_open["Size"].unique():
    # Take the row where the number of processors is equal to n
    tmp_mpi       = df_mpi[df_mpi["np"] == n]
    tmp_true      = df_true[df_true["np"] == n]
    tmp_open      = df_open[df_open["np"] == n]
    
    # Plot the curves
    plt.cla()
    plt.plot(tmp_mpi ["Size"].unique(), tmp_mpi["Latency (ns)"], label="MPI")
    plt.plot(tmp_true["Size"].unique(), tmp_true["Latency (ns)"], label="MPI_true")
    plt.plot(tmp_open["Size"].unique(), tmp_open["Latency (ns)"], label="OpenMP")

    # Set the plot's informations
    plt.title(f"Size:{n}")  
    plt.xlabel("np")
    plt.ylabel("Latency (ns)")
    
    # Set additional informations
    plt.xticks(tmp_open["np"].unique())
    plt.grid()
    plt.legend()
    
    # Save the plots
    plt.savefig(f"plots/Size:{n}.png")
