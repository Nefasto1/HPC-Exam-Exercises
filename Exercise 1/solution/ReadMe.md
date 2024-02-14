# Exercise 1

To launch the commands to obtain the times in slurm use the command:

```sbatch get_latency.job <num>```

```sbatch fixed_size_thin.job <num>```

```sbatch p2p_latency.job```

where:
  - `<num>` is the iteration's number to execute

To preprocess the data launch the `preprocess.py` code using the command:

```python preprocess.py```

Before to plot the results check that exists the directories "plots" and "inverted_plots" inside the directory in which the next command will be executed.
In the end, to plot the results, use the command:

```python plot.py```
or
```python plot_inverted.py```
