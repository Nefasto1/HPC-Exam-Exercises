import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import warnings
warnings.filterwarnings('ignore') 

# Open the point to point dataset informations
df_lat_core = pd.read_csv("results/latency_different_core_preprocessed.txt")
df_lat_sock = pd.read_csv("results/latency_different_socket_preprocessed.txt")
df_lat_node = pd.read_csv("results/latency_different_node_preprocessed.txt")

# Sepatate the plots for the classic thin node and the fixed size message thin
for name in ["thin", "fixed_thin"]:
    # Open the dataframe
    df = pd.read_csv(f"results/results_{name}_merged.txt", sep="\t")

    # Each type of communication routine will have its own plot
    for type in ["broadcast", "scatter"]:
        # For each size
        for n in df["Size"].unique():
            # Create a new plot
            plt.cla()
            fig, ax = plt.subplots()

            # For each implementation
            for alg in df["Algorithm"].unique():
                if type in alg:
                    # Select the correct rows
                    npvect  = (df["Size"] == n).values
                    algvect = (df["Algorithm"] == alg).values
                    idxs    = [n and alg for n, alg in zip(npvect, algvect)]

                    # Calculate the mean and the standard deviations grouping by mean
                    nps = np.sort(df[idxs]["np"].unique())
                    vals = [df[idxs][df["np"] == i]["Latency (us)"].values for i in nps]
                    means = df[idxs].groupby("np")["Latency (us)"].mean().values
                    stds = df[idxs].groupby("np")["Latency (us)"].std().values

                    y_errs = [sd * np.sqrt(1/len(x)) * 1.96 for sd, mean, x in zip(stds, means, vals)]

                    # Plot the curves
                    ax.plot(nps, means, '-', label=alg)
                    ax.fill_between(nps, means - stds, means + stds, alpha=0.2)
            
            # Plot the naive algorithm
            lat_core = df_lat_core[df_lat_core["Size"] == n]["Latency (us)"].values[0]
            lat_sock = df_lat_sock[df_lat_sock["Size"] == n]["Latency (us)"].values[0]
            lat_node = df_lat_node[df_lat_node["Size"] == n]["Latency (us)"].values[0]
            
            naive = [lat_core*(p - (p>12) - (p>24) - (p>36) -1) + lat_sock*(p>12) + lat_node*(p>24) + lat_sock*(p>36) for p in nps]
                
            plt.plot(nps, np.array(naive), label="Naive")
                
            # Add some other configurations
            plt.xlim((0, 49))
            plt.xticks(list(range(0, 49, 10)) + [12, 24, 36, 48])
                
            plt.axvline(x=12, color='gray')    
            plt.axvline(x=24, color='gray')    
            plt.axvline(x=36, color='gray')  
            
            plt.title(f"Size={n}")
            plt.legend()
            plt.grid()
            plt.xlabel("# Cores")
            plt.ylabel("Latency (us)")
            plt.savefig(f"plots/{name} - {type} - Size={n}.png")
            plt.close()