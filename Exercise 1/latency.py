import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

place = "core"
node = "epyc"

# df_lat = pd.read_csv(f"results/latency_different_{place}_{node}_preprocessed.txt", sep="\t")
df_bro = pd.read_csv(f"results/results_{node}_merged.txt", sep="\t")

npvect  = (df_bro["np"] == 2).values
algvect = (df_bro["Algorithm"] == df_bro["Algorithm"].unique()[0]).values
idxs    = [n and alg for n, alg in zip(npvect, algvect)]


mean_bro = df_bro[idxs].groupby("Size")["Latency (us)"].mean()
# mean_lat = df_lat.groupby("Size")["Latency"].mean()

# gamma = mean_bro / mean_lat
# gamma = gamma.dropna()

# print(df_bro["Algorithm"].unique())

# test = gamma * mean_lat[1:-2]

# plt.plot(df_bro["Size"].unique(), mean_bro.values, label="Observed")
# plt.plot(df_bro["Size"].unique(), test.values)
# plt.grid()
# plt.legend()
# plt.savefig("prova.png")

print(df_bro.head())

X = df_bro.drop(["Latency (us)"], axis=1).values
y = df_bro["Latency (us)"].values

clf = LinearRegression().fit(X, y)

test = np.array([df_bro["Size"].unique(), [2]*len(df_bro["Size"].unique()), ["broadcast_flat"]*len(df_bro["Size"].unique())])


pred = clf.predict(test)

plt.plot(df_bro["Size"].unique(), pred, label="Predicted")
plt.plot(df_bro["Size"].unique(), mean_bro.values, label="True")

plt.grid()
plt.legend()
plt.savefig("prova.png")
