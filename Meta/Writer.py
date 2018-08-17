import numpy
import math
from sortedcontainers import SortedDict
import random
import numpy 
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import os

#Defaults:

#timeline = SortedDict()
t_max = 12*10 #12 * 30 # time when simulation ends

# MALES
males = 50 # number of male birds

# FEMALES
F_per_M = 3 #The number of sexualy mature females per sexually mature male
females = males * F_per_M # number of female birds
female_visit_param = [0, t_max / 2.0] # females visit early in the period

# POSITIONS AND TRAVEL TIME
x_dim, y_dim = 1000, 1000 # dimensions of environment
bird_speed = 12 * 3600 # m/hr (12 m/s)
# now choose lambda_dist, controlling the probability of traveling to a neighbor
# the probability of choosing a neighbor at distance x is proportional to exp(-\lambda x)
# choose lambda such that 99% of the mass is before 800 meters
improb_dist = 800
improb_sds = 2
#if using exp decay
#lambda_dist = - math.log(1.0 - improb) / improb_distance


# ACTION DISTRIBUTIONS
# Time of forage
FG_tau_mean, FG_tau_std = .4, .167 #mean and sd of truncated normal distribution rv to find a male's time until next FG
FG_tau_range = [0, 1] #maximum and minimum FG taus
FG_tau_norm_range = [(FG_tau_range[0] - FG_tau_mean) / FG_tau_std, (FG_tau_range[1] - FG_tau_mean) / FG_tau_std] #normalized
# Duration of forage
FG_k=1.5 #the shape of the gamma distribution rv used to generate FG taus
FG_theta=5 #the scale of the gamma distribution rv used to generate FG taus
FG_divisor=60 #helps scale gamma distritbution
# Duration of repair bower / stay at bower
RBSB_tau_mean, RBSB_tau_std = .1583, .09755 #mean and sd of truncated normal distribution rv to find duration of repair bower / stay at bower
RBSB_tau_range = [0,.5] #maximum and minimum taus
RBSB_tau_norm_range = [(RBSB_tau_range[0] - RBSB_tau_mean) / RBSB_tau_std, (RBSB_tau_range[1] - RBSB_tau_mean) / RBSB_tau_std] #normalized

damage_to_bower = 6.0

#Male strategies
C_or_D='C'

max_maraud=0.15
strategies_string = 'numpy.random.random(males)*{}'.format(max_maraud)


num_sims=5

name_vec=['t_max', 
          'males', 
          'F_per_M', 
          'females', 
          'female_visit_param',
          'x_dim', 
          'y_dim', 
          'bird_speed', 
          'improb_dist',
          'improb_sds', 
          'FG_tau_mean', 
          'FG_tau_std',
          'FG_tau_range', 
          'FG_tau_norm_range', 
          'FG_k', 
          'FG_theta', 
          'FG_divisor',
          'RBSB_tau_mean', 
          'RBSB_tau_std', 
          'RBSB_tau_norm_range',
          'damage_to_bower',
          #'prop_marauder'
         ]
value_vec=[t_max, 
          males, 
          F_per_M, 
          females, 
          female_visit_param,
          x_dim, 
          y_dim, 
          bird_speed, 
          improb_dist,
          improb_sds,
          FG_tau_mean, 
          FG_tau_std,
          FG_tau_range, 
          FG_tau_norm_range, 
          FG_k, 
          FG_theta, 
          FG_divisor,
          RBSB_tau_mean, 
          RBSB_tau_std, 
          RBSB_tau_norm_range,
          damage_to_bower
         ]

in_titles=[]
for j in range(num_sims):
    output_title='res_{}_{}_strat={}_dim={}_repair {}.csv'.format(j,C_or_D,max_maraud,x_dim,damage_to_bower)
    my_string='random_seed = ' + str(j) + '\n'+'output_title = ' + "'" + output_title + "'" + '\n' + 'strategies_string =' + "'" + strategies_string + "'" + '\n'
    for i in range(len(name_vec)):
        tack_on= str(name_vec[i]) + ' = ' + str(value_vec[i]) + '\n'
        my_string+=tack_on
#with open("descriptive_name_{}.py".format(j), "w") as f:
    in_title="in_{}_{}_strat={}_dim={}_repair={}".format(j,C_or_D,max_maraud,x_dim,damage_to_bower)
    in_titles.append(in_title)
    with open(in_title,"w") as f:
        f.write(my_string)
print(in_titles)


#for j in range(num_sims):
#    os.remove("in_{}_{}_strat={}_dim={}_repair={}".format(j,C_or_D,max_maraud,x_dim,damage_to_bower))
    