import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("prova.txt", sep="\t")

for n in df["Size"].unique():
    idxs = (df["Size"] == n).values
    plt.plot(df[idxs]["np"], df[idxs]["Latency (ns)"], label=n)
    
plt.xlabel("# Threads")
plt.ylabel("Latency (ns)")
plt.legend()
plt.grid()
plt.xticks([2**i for i in range(int(np.log2(128*4)))])
plt.savefig("prova.png")
