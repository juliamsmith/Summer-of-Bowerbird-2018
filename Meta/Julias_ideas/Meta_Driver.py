import os
import shutil
from Writer import in_write
#from Batch_func import BnS

def vary_params(dim_vec, m_prop_vec, RB_time_vec, num_sims):
    for i in range(len(dim_vec)):
        dim_val = dim_vec[i]
        for j in range(len(m_prop_vec)):
            m_prop_val = m_prop_vec[j]
            for k in range(len(RB_time_vec)):
                RB_time_val = RB_time_vec[k] 
                #####THIS IS THE UNIT WE WANT TO BE ONE BATCH (or so we thought): 1000 sims, 100 males, t_max 12*30 takes 6.67hrs or 24s/sim
                #in_write writes input files and creates a folder called conditions_name with param and res folders inside
                [in_titles, out_titles, conditions_name] = in_write(dim_val, m_prop_val, RB_time_val, num_sims)
                #writer puts them in a input folder.. try to run one input file tomorrow
                for l in range(len(in_titles)):
                    in_title = in_titles[l]
                    out_title = out_titles[l]
                    os.system("python3 bowerbird_prog.py {}".format(in_title))
                    # incorporate batch stuff properly -- BnS(script, JobName, queue=Q)
                    # I believe 1000 sims (or one set of conditions) is a batch
                    #perhaps the ideal script is the 1000sims (so just outside of this for loop)
                    shutil.move(in_title, "{}/parameters".format(conditions_name))
                    shutil.move(out_title, "{}/results".format(conditions_name))
                    
                    
# #!/bin/bash
# #SBATCH --job-name=conditions_name
# #SBATCH --time=07:00:00
# #SBATCH --partition=broadwl
# #SBATCH --nodes=1
# #SBATCH --ntasks-per-node=1
# #SBATCH --mem-per-cpu=2000

# module load Anaconda3/5.1.0
# mpirun ./the_code_below_the_comment.py