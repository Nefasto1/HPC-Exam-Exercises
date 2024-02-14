import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Open the dataframes
df_true   = pd.read_csv(f"results/True.txt", sep="\t")
df_open   = pd.read_csv(f"results/b_cast_openmp.txt", sep="\t")
df_flat   = pd.read_csv(f"results/flat.txt", sep="\t")
df_chain  = pd.read_csv(f"results/chain.txt", sep="\t")
df_binary = pd.read_csv(f"results/binary.txt", sep="\t")

# Plot the Algorithms' Latency in function of the number of processors
for n in df_open["np"].unique():
    # Take the row where the number of processors is equal to n
    tmp_true   = df_true[df_true["np"] == n]
    tmp_open   = df_open[df_open["np"] == n]
    tmp_flat   = df_flat[df_flat["np"] == n]
    tmp_chain  = df_chain[df_chain["np"] == n]
    tmp_binary = df_binary[df_binary["np"] == n]
    
    # Plot the curves
    plt.cla()
    plt.plot(np.log2(tmp_true["Size"].unique()),    tmp_true["Latency (ns)"]/1000, label="MPI True")
    plt.plot(np.log2(tmp_open["Size"].unique()),    tmp_open["Latency (ns)"]/1000, label="OpenMP")
    plt.plot(np.log2(tmp_flat ["Size"].unique()),   tmp_flat["Latency (ns)"]/1000, label="Flat")
    plt.plot(np.log2(tmp_chain ["Size"].unique()),  tmp_chain["Latency (ns)"]/1000, label="Chain")
    plt.plot(np.log2(tmp_binary ["Size"].unique()), tmp_binary["Latency (ns)"]/1000, label="Binary")

    # Set the plot's informations
    plt.title(f"np:{n}")  
    plt.xlabel("log2 Size")
    plt.ylabel("Time (us)")
    
    # Set additional informations
    plt.xticks(np.log2(tmp_open["Size"].unique()))
    plt.grid()
    plt.legend()
    
    # Save the plots
    plt.savefig(f"plots/np:{n}.png")
    
