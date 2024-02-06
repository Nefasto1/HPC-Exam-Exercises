import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Separate the thin plots to the fixed size thin plots
for name in ["thin", "fixed_thin"]:

    # Open the dataframe
    df = pd.read_csv(f"results/results_{name}_merged.txt", sep="\t")

    # Each communication routine will have its own plot
    for type in ["broadcast", "scatter"]:
        # For each size
        for n in df["Size"].unique():
            
            # Create a new plot
            plt.cla()
            fig, ax = plt.subplots()

            for alg in df["Algorithm"].unique():
                if type in alg:
                    # Select the correct rows
                    npvect  = (df["Size"] == n).values
                    algvect = (df["Algorithm"] == alg).values
                    idxs    = [n and alg for n, alg in zip(npvect, algvect)]

                    # Calculate the mean and the standard deviations 
                    nps = df[idxs]["np"].unique()
                    vals = [df[idxs][df["np"] == i]["Latency (us)"].values for i in nps]
                    means = df[idxs].groupby("np")["Latency (us)"].mean().values
                    stds = df[idxs].groupby("np")["Latency (us)"].std().values

                    y_errs = [sd * np.sqrt(1/len(x)) * 1.96 for sd, mean, x in zip(stds, means, vals)]

                    # Take the logarithm of the number of processors
                    nps = np.log2(nps)

                    # Plot the curves
                    ax.plot(nps, means, '-', label=alg)
                    ax.fill_between(nps, means - stds, means + stds, alpha=0.2)

            # Add some configurations
            plt.title(f"Size={n}")
            plt.legend()
            plt.grid()
            plt.xlabel("# Cores")
            plt.ylabel("Latency (us)")
            plt.savefig(f"plots_log/{name} - {type} - Size={n}.png")
            plt.close()