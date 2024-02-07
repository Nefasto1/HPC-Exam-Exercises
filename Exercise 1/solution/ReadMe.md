To launch the commands to obtain the times in slurm use the command:

```sbatch <.job file> <num>```

where:
  - <.job file> is equal to "code_thin.job", "fixed_size_thin.job" or "latency_thin.job"
  - <num> is the number of the iteration to execute, it is mandatory only for "code_thin.job" and "fixed_size_thin.job"

Before to run the code you must ensure to create the directories `~/exam/results` where the data will be saved, or change the paths in the code.


