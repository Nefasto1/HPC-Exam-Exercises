# Substitute the results spaces with a tab
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

# for i in ["core", "socket", "node"]: 
#         with open(f"results/latency_different_{i}_thin.txt", "r") as f:
#                 string = f.readlines()

#         newstring = [string[0]]
#         for row in string[2:]:
#                 tmp = row.split(" ")
#                 row = tmp[0] + "\t" + tmp[-1]
#                 newstring.append(row)

#         with open(f"latency_different_{i}_preprocessed.txt", "w") as f:
#                 f.writelines(newstring)


#         with open(f"results/results_epyc_{i}.txt", "r") as f:
#                 string = f.readlines()

#         newstring = [string[0]]
#         for row in string[2:]:
#                 tmp = row.split(" ")
#                 row = tmp[0] + "\t" + tmp[-1]
#                 newstring.append(row)

#         with open(f"results/results_epyc_preprocessed_{i}.txt", "w") as f:
#                 f.writelines(newstring)

# for i in range(1, 11): 
#         with open(f"results/fixed_thin_{i}.txt", "r") as f:
#                 string = f.readlines()

#         newstring = [string[0]]
#         for row in string[2:]:
#                 tmp = row.split(" ")
#                 row = tmp[0] + "\t" + tmp[-1]
#                 newstring.append(row)

#         with open(f"results/fixed_thin_preprocessed_{i}.txt", "w") as f:
#                 f.writelines(newstring)
                
# #         with open(f"results/fixed_epyc_{i}.txt", "r") as f:
# #                 string = f.readlines()

# #         newstring = [string[0]]
# #         for row in string[2:]:
# #                 tmp = row.split(" ")
# #                 row = tmp[0] + "\t" + tmp[-1]
# #                 newstring.append(row)

# #         with open(f"results/fixed_epyc_preprocessed_{i}.txt", "w") as f:
# #                 f.writelines(newstring)

# merge the results
import pandas as pd

# epyc = [pd.read_csv(f"results/results_epyc_preprocessed_{i}.txt", sep="\t") for i in range(1, 11)]
thin = [pd.read_csv(f"results/results_thin_preprocessed_{i}.txt", sep="\t") for i in range(1, 3)]

# # fixed_epyc = [pd.read_csv(f"results/fixed_epyc_preprocessed_{i}.txt", sep="\t") for i in range(1, 11)]
# fixed_thin = [pd.read_csv(f"results/fixed_thin_preprocessed_{i}.txt", sep="\t") for i in range(1, 11)]

# # merged_epyc = pd.concat(epyc)
merged_thin = pd.concat(thin)

# # merged_fixed_epyc = pd.concat(fixed_epyc)
# merged_fixed_thin = pd.concat(fixed_thin)

# # merged_epyc.to_csv("results/results_epyc_merged.txt", sep="\t", index=False)
merged_thin.to_csv("results/results_thin_merged.txt", sep="\t", index=False)

# # merged_fixed_epyc.to_csv("results/results_fixed_epyc_merged.txt", sep="\t", index=False)
# merged_fixed_thin.to_csv("results/results_fixed_thin_merged.txt", sep="\t", index=False)


# # import pandas as pd

# # thin = [pd.read_csv(f"results/results_thin_preprocessed_{i}.txt", sep="\t") for i in range(1, 11)]

# # fixed_thin = [pd.read_csv(f"results/fixed_thin_preprocessed_{i}.txt", sep="\t") for i in range(1, 11)]

# # merged_thin = pd.concat(thin)

# # merged_thin.loc[merged_thin["Algorithm"] == "scatter_binomial", "Algorithm"] = "scatter_nb"
# # merged_thin.loc[merged_thin["Algorithm"] == "scatter_basic_linear","Algorithm"] = "scatter_binomial"
# # merged_fixed_thin = pd.concat(fixed_thin)

# # merged_thin.to_csv("results/results_thin_merged.txt", sep="\t", index=False)

# # merged_fixed_thin.to_csv("results/results_fixed_thin_merged.txt", sep="\t", index=False)