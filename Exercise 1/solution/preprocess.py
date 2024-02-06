# Substitute all the spaces inside the results with a tab
for i in range(1, 10): 
        with open(f"results/results_thin_{i}.txt", "r") as f:
                string = f.readlines()

        newstring = [string[0]]
        for row in string[2:]:
                tmp = row.split(" ")
                row = tmp[0] + "\t" + tmp[-1]
                newstring.append(row)

        with open(f"results/results_thin_preprocessed_{i}.txt", "w") as f:
                f.writelines(newstring)

# Substitute all the spaces inside the latency results with a tab
for i in ["core", "socket", "node"]: 
        with open(f"results/latency_different_{i}_thin.txt", "r") as f:
                string = f.readlines()

        newstring = [string[0]]
        for row in string[2:]:
                tmp = row.split(" ")
                row = tmp[0] + "\t" + tmp[-1]
                newstring.append(row)

        with open(f"latency_different_{i}_preprocessed.txt", "w") as f:
                f.writelines(newstring)


        with open(f"results/results_epyc_{i}.txt", "r") as f:
                string = f.readlines()

        newstring = [string[0]]
        for row in string[2:]:
                tmp = row.split(" ")
                row = tmp[0] + "\t" + tmp[-1]
                newstring.append(row)

        with open(f"results/results_epyc_preprocessed_{i}.txt", "w") as f:
                f.writelines(newstring)

# Substitute all the spaces inside the results with a tab
for i in range(1, 11): 
        with open(f"results/fixed_thin_{i}.txt", "r") as f:
                string = f.readlines()

        newstring = [string[0]]
        for row in string[2:]:
                tmp = row.split(" ")
                row = tmp[0] + "\t" + tmp[-1]
                newstring.append(row)

        with open(f"results/fixed_thin_preprocessed_{i}.txt", "w") as f:
                f.writelines(newstring)
                

# merge the results
import pandas as pd

thin = [pd.read_csv(f"results/results_thin_preprocessed_{i}.txt", sep="\t") for i in range(1, 3)]
fixed_thin = [pd.read_csv(f"results/fixed_thin_preprocessed_{i}.txt", sep="\t") for i in range(1, 11)]

merged_thin = pd.concat(thin)
merged_fixed_thin = pd.concat(fixed_thin)

merged_thin.to_csv("results/results_thin_merged.txt", sep="\t", index=False)
merged_fixed_thin.to_csv("results/results_fixed_thin_merged.txt", sep="\t", index=False)