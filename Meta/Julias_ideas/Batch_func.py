## function to Build and Submit to Midway Research Computing Cluster
#BnS <- function(script, JobName, queue=Q) {
#to_submit <- paste("#!/bin/bash\n#SBATCH -J", JobName,
#"\n#SBATCH -p sandyb",
#"\n#SBATCH --ntasks-per-node=8",
#"\n\n module load R/3.2\n", script)
#if (queue == 'none') {
#cat(to_submit, "\n\n")
#} else if (queue == 'local') {
#system(script)
#} else {
#ff <- file(JobName)
#writeLines(to_submit, ff)
#close(ff)
#system(paste('sbatch', JobName))
#Sys.sleep(1)
#}
#return(0)
#}


def BnS(script, JobName, queue=Q):
    to_submit = ("#!/bin/bash\n#SBATCH -J " + JobName + 
    "\n#SBATCH -p sandyb" + 
    "\n#SBATCH --ntasks-per-node=8" + 
    "\n\nmodule load Python3\n" + script)
    if queue == 'none':
        "to_submit"+"\n\n"
    elif queue == 'local':
        os.system(script)
    else:
        with open(JobName,"w") as f:
            f.write(to_submit)
        os.system("sbatch " + JobName)
        Sys.sleep(1)
    #return(0)
    
    