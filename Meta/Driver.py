#import numpy 
#import sys # this is needed for command line arguments
#import imp # this is to import modules from strings
import os
#import math
#from sortedcontainers import SortedDict
#import random
#import matplotlib.pyplot as plt
#from scipy.stats import truncnorm
#import csv
#import copy
from Writer import in_titles
from Writer import output_titles
from Writer import conditions_name
import shutil


if __name__ == "__main__":
    global in_titles
    for i in range(len(in_titles)):
        in_title=in_titles[i]
        output_title=output_titles[i]
        os.system("python3 bowerbird_prog.py {}".format(in_title))
        shutil.move(in_title, "{}/parameters".format(conditions_name))
        shutil.move(output_title, "{}/results".format(conditions_name))
        
        
    