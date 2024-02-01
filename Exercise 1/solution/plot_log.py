import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

for name in ["thin", "fixed_thin"]: #"fixed_epyc"]:

    df = pd.read_csv(f"results/results_{name}_merged.txt", sep="\t")

    for type in ["broadcast", "scatter"]:
        for n in df["Size"].unique():
            plt.cla()
            fig, ax = plt.subplots()

            for alg in df["Algorithm"].unique():
                if type in alg:
                    npvect  = (df["Size"] == n).values
                    algvect = (df["Algorithm"] == alg).values
                    idxs    = [n and alg for n, alg in zip(npvect, algvect)]

                    nps = df[idxs]["np"].unique()
                    vals = [df[idxs][df["np"] == i]["Latency (us)"].values for i in nps]
                    means = df[idxs].groupby("np")["Latency (us)"].mean().values
                    stds = df[idxs].groupby("np")["Latency (us)"].std().values

                    y_errs = [sd * np.sqrt(1/len(x)) * 1.96 for sd, mean, x in zip(stds, means, vals)]

                    nps = np.log2(nps)

                    ax.plot(nps, means, '-', label=alg)
                    ax.fill_between(nps, means - stds, means + stds, alpha=0.2)
                    # plt.plot(df[idxs]["np"], df[idxs]["Latency (us)"], label=alg)
                
            # if name == "epyc": 
            #     half = 128
            #     plt.xticks([2**i for i in range(int(np.log2(half*4)))])
            # else:
            #     half = 36
            #     plt.xticks([3] + [9*2**i for i in range(4)])
            # plt.axvline(x=half, color='red')    
            plt.title(f"Size={n}")
            plt.legend()
            plt.grid()
            plt.xlabel("# Cores")
            plt.ylabel("Latency (us)")
            plt.savefig(f"plots_log/{name} - {type} - Size={n}.png")
            plt.close()

# df = pd.read_csv(f"results_epyc_merged.txt", sep="\t")


# npvect  = (df["Size"] == 2).values
# algvect = (df["Algorithm"] == "broadcast_flat").values
# idxs    = [n and alg for n, alg in zip(npvect, algvect)]

# nps = df[idxs]["np"].unique()
# vals = [df[idxs][df["np"] == i]["Latency (us)"].values for i in nps]
# means = df[idxs].groupby("np")["Latency (us)"].mean().values
# stds = df[idxs].groupby("np")["Latency (us)"].std().values


# y_errs = [sd * np.sqrt(1/len(x)) * 1.96 for sd, mean, x in zip(stds, means, vals)]


# fig, ax = plt.subplots()
# ax.plot(nps, means, '-')
# ax.fill_between(nps, means - stds, means + stds, alpha=0.2)
# fig.savefig("prova.png")