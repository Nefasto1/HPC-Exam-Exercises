import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Open the dataframes
df_true      = pd.read_csv(f"results/True.txt", sep="\t")
df_open      = pd.read_csv(f"results/b_cast_openmp.txt", sep="\t")
df_flat      = pd.read_csv(f"results/flat.txt", sep="\t")
df_chain     = pd.read_csv(f"results/chain.txt", sep="\t")
df_binary    = pd.read_csv(f"results/binary.txt", sep="\t")

# Plot the Algorithms' Latency in function of the number of processors
for n in df_open["Size"].unique():
    # Take the row where the number of processors is equal to n
    tmp_true      = df_true[df_true["Size"] == n]
    tmp_open      = df_open[df_open["Size"] == n]
    tmp_flat      = df_flat[df_flat["Size"] == n]
    tmp_chain     = df_chain[df_chain["Size"] == n]
    tmp_binary    = df_binary[df_binary["Size"] == n]
    
    # Plot the curves
    plt.cla()
    plt.plot(tmp_true["np"].unique(),    tmp_true  ["Latency (ns)"]/1000, label="MPI True")
    plt.plot(tmp_open["np"].unique(),    tmp_open  ["Latency (ns)"]/1000, label="OpenMP")
    plt.plot(tmp_flat ["np"].unique(),   tmp_flat  ["Latency (ns)"]/1000, label="Flat")
    plt.plot(tmp_chain ["np"].unique(),  tmp_chain ["Latency (ns)"]/1000, label="Chain")
    plt.plot(tmp_binary ["np"].unique(), tmp_binary["Latency (ns)"]/1000, label="Binary")

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
    
