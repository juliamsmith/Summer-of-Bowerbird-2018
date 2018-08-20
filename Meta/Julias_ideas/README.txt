#NOTES
This runs multiple conditions.  In Meta_Driver, we work through all the combinations of parameter values we want to try.  Currently, to make changes, edit terminal_call (modify the vectors of values for parameters we want to vary as well as the number of simulations) and, more rarely, Writer (to modify defaults for other things... t_max, number of males, etc.).
I haven't incorporated the midway-job-specific code, although I have tried to put the R code you sent in Python (see "Batch_func").  Didn't know exactly where to work it in, though. 


#To run (at the point when it actually runs -- right now it needs work):
python3 terminal_call.py