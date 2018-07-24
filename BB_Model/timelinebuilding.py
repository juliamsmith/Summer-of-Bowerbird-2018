import math
import random
import numpy as numpy
import matplotlib.pyplot as plt


#Parameters:
t=0.0 #start at time 0
t_max=12#12*4*30 #2 months in hrs (assume no nights so 12 hr = 1 day)
bird_speed=12*3600 #m/hr (12m/s)
d=150.0
nodes=4
FV_param=[1, t_max/2] #5days, tmax/3 #0.2 #nodes/0.19 #totally random
FG_param=3 #larger values lead to foraging ending earlier, because taus are smaller
SB_param=1.5 #larger values lead to bowerstay ending earlier, because taus are smaller
RB_param=2 #made up -- takes 30mins (every time -- no distribution) to repair bower
MA_param=.1 #made up -- takes 6mins (every time -- no distribution) to maraud bower
timeline=[]


def ticketgenerator(tau,t, o, a, targ, t2):
    ticket={
        'tau': tau, #how long the activity lasts
        'time': t, #time at which the activity starts
        'owner': o, #who is doing the activity (could be a female if action=-3)
        'action': a, #which activity (see key)
        'target': targ, #target of the activity (owner=target unless action=-3,-4,-5, or -6)
        'origin': t2 #the time of the ticket that generated this one
    }
    return ticket;

#adds new tickets to timeline -- Stefano, any more efficient suggestions for keeping timeline in order?
def addtotimeline(tic): #A CHANGE
    if not timeline:
        timeline.append(tic)
    else:
        ind=len(timeline)-1
        end=0
        while (tic['time']<timeline[ind]['time'] and end==0): #moves backwards until it finds where to place the ticket based on the listed times
            ind=ind-1 
            if(ind<0):
                end=1
        ind=ind+1
        timeline.insert(ind, tic)


#travel time
#distance function
def travel(nodes,d,bird_speed):
    node_dist= numpy.array([[-1.0]*nodes]*nodes) #(dist in m)initialize a nodes-by-nodes matrix (1st nrows, 2nd ncols)
    sqrt_nodes=int(math.sqrt(nodes)) 
    node_graph=numpy.arange(nodes)
    node_mat=node_graph.reshape(sqrt_nodes,sqrt_nodes)
    for i in range(sqrt_nodes):
        for j in range (sqrt_nodes):
            n1=node_mat[i][j]
            for a in range(sqrt_nodes):
                for b in range(sqrt_nodes):
                    n2=node_mat[a][b]
                    if n1<n2:
                        d12=math.hypot((i-a)*d,abs(j-b)*d)
                        node_dist[n1][n2]=d12
                        node_dist[n2][n1]=d12
                    if n1==n2:
                        node_dist[n1][n2]=0
    travel_times=numpy.array([[0.0]*nodes]*nodes)
    for i in range(nodes):
        for j in range(nodes):
            travel_times[i][j]=node_dist[i][j]/bird_speed
    return [node_dist,travel_times, node_mat]




travel_mats=travel(nodes,d,bird_speed)
travel_times=travel_mats[1]



# function for determining the next time based on our rate parameters
def nexttau(action, ow, targ, new_t):
    new_tau=-1
    while new_tau<=0:
        switcher = { #NOTE: used abs
            -1: numpy.random.normal(loc=.1583, scale=.09755, size=1)[0], #choose when to leave bower (generate a tau for bower stay)
            -2: numpy.random.gamma(shape=1.5, scale=5, size=1)[0]/60, #choose when to stop foraging (generate a tau for foraging)
            -3: numpy.random.uniform(FV_param[0], FV_param[1]), #FV_param... totally arbitrary so we should think about it
            -4: travel_times[ow][targ],
            -5: MA_param, #in the future we'll do something with it
            -6: travel_times[targ][ow],
            -7: RB_param #in the future we'll do something with it 
        }
        new_tau=switcher.get(action)
    future_t=new_tau+new_t #time on future ticket will be the current time plus the tau
    if future_t>t_max: 
        new_tau=(new_tau-(future_t-t_max)) #this ensures that the tau+t won't exceed t_max
    return new_tau

def futurebuilder(old_tic, new_ac, new_targ):
    old_t=old_tic['time']
    new_t=old_t+old_tic['tau']
    new_tic={}
    if new_t<t_max:
        ow=old_tic['owner']
        new_tic=ticketgenerator(nexttau(new_ac, ow, new_targ, new_t), new_t, ow, new_ac, new_targ, old_t)
        addtotimeline(new_tic)
    return new_tic
    
    
#solve for lambda 
improb=0.99
improb_distance=800
lamb=-math.log(1-improb)/improb_distance

#will write female preference based on cumulative exponential decay (lambda=.00576)
def femaleprobs(node_dist, nodes, lamb):
    visit_preferences=numpy.array([[0.]*nodes]*nodes)
    for i in range(nodes):
        for j in range(nodes):
            if i!=j:
                visit_preferences[i][j]=math.exp(-lamb*node_dist[i][j])        
        visit_preferences[i]=visit_preferences[i]/sum(visit_preferences[i])
    return visit_preferences

visit_preferences=femaleprobs(travel_times, nodes, lamb)

