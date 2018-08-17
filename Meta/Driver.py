import numpy 
import sys # this is needed for command line arguments
import imp # this is to import modules from strings
import os
import math
from sortedcontainers import SortedDict
import random
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import csv
import copy
from Writer import in_titles

if __name__ == "__main__":
    global in_titles
    for i in in_titles:
        os.system("python3 bowerbird_prog.py {}".format(i))
    