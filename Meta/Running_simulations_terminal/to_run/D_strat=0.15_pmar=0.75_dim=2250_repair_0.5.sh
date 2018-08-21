#!/bin/bash
#SBATCH -J D_strat=0.15_pmar=0.75_dim=2250_repair_0.5.sh
#SBATCH --time=07:00:00
#SBATCH -p broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

module load Anaconda3/5.1.0
python3 bowerbird_prog.py D_strat=0.15_pmar=0.75_dim=2250_repair_0.5/parameters/in_0D_strat=0.15_pmar=0.75_dim=2250_repair_0.5
mv res_0D_strat=0.15_pmar=0.75_dim=2250_repair_0.5.csv D_strat=0.15_pmar=0.75_dim=2250_repair_0.5/results/res_0D_strat=0.15_pmar=0.75_dim=2250_repair_0.5.csv
python3 bowerbird_prog.py D_strat=0.15_pmar=0.75_dim=2250_repair_0.5/parameters/in_1D_strat=0.15_pmar=0.75_dim=2250_repair_0.5
mv res_1D_strat=0.15_pmar=0.75_dim=2250_repair_0.5.csv D_strat=0.15_pmar=0.75_dim=2250_repair_0.5/results/res_1D_strat=0.15_pmar=0.75_dim=2250_repair_0.5.csv
