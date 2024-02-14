# Exercise 1

To launch the commands to obtain the times in slurm use the command:

```sbatch <.job file> <num>```

where:
  - `<.job file>` is equal to "get_latency.job", "fixed_size_thin.job" or "p2p_latency.job"
  - `<num>` is the number of the iteration to execute, it is mandatory only for "code_thin.job" and "fixed_size_thin.job"

To preprocess the data launch the `preprocess.py` code using the command:

```python preprocess.py```

Before to plot the results check that exists the directories "plots" and "inverted_plots" inside the directory in which the next command will be executed.
In the end, to plot the results, use the command:

```python plot.py```
or
```python plot_inverted.py```
