import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

name = "thin"
df = pd.read_csv(f"results/results_{name}_merged.txt", sep="\t")

# Each communication routine will have its own plot
for type in ["broadcast", "scatter"]:
    
    # For each number of processors
    for n in df["np"].unique():
        
        # Create the plot
        plt.cla()
        fig, ax = plt.subplots()

        # For each implementation
        for alg in df["Algorithm"].unique():
            if type in alg:
                # Take the results relative to this information
                npvect  = (df["np"] == n).values
                algvect = (df["Algorithm"] == alg).values
                idxs    = [n and alg for n, alg in zip(npvect, algvect)]

                # Calculate mean and standard deviation grouping by Size
                nps = df[idxs]["Size"].unique()
                vals = [df[idxs][df["Size"] == i]["Latency (us)"].values for i in nps]
                means = df[idxs].groupby("Size")["Latency (us)"].mean().values
                stds = df[idxs].groupby("Size")["Latency (us)"].std().values

                y_errs = [sd * np.sqrt(1/len(x)) * 1.96 for sd, mean, x in zip(stds, means, vals)]

                # Plot the curves
                ax.plot(nps, means, '-', label=alg)
                ax.fill_between(nps, means - stds, means + stds, alpha=0.2)

        # Add some configurations
        plt.xticks(nps)

        plt.title(f"np={n}")
        plt.legend()
        plt.grid()
        plt.xlabel("Size")
        plt.ylabel("Latency (us)")
        plt.savefig(f"plots_inverted/{name} - {type} - np={n}.png")
        plt.close()