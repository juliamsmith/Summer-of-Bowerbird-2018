from timelinebuilding import ticketgenerator
from timelinebuilding import addtotimeline
from timelinebuilding import travel
from timelinebuilding import ticketgenerator
from timelinebuilding import nexttau
from timelinebuilding import futurebuilder
from timelinebuilding import femaleprobs

timeline=[]

#Stay at bower ticket handler. Ticket is read, and male state changes to at bower. 
#The tickethandler can generate then generate a repair bower, foraging, or maurad travel ticket.
def SBtickethandler(SB_tic):
    ow=SB_tic['owner'] #the owner of the ticket is the male bird from the stay at bower ticket
    if male_states[ow]!=0: #because any male who is at his bower was last repairing his bower (not coming from foraging or maurading) 
        bower_states[ow]=1 #now the bower is intact, so the bower state is updated to reflect this change
    if bower_states[ow]==0: #if male returns to a destroyed bower, must repair it
        new_tic=futurebuilder(SB_tic, -7, ow) #generate a new tau and ticket with repair bower action, and add it to the timeline
    else: #if the bower is intact
        decider=random.random()
        if decider<MT_vs_FG: #transition to MT
            targ=numpy.random.choice(list(range(nodes)), p=visit_preferences[ow]) #choosing the male to maurad based on visit preferences
            new_tic=futurebuilder(SB_tic, -4, targ) #generate a new tau and ticket with maurad travel action, and add it to the timeline
        else:
            new_tic=futurebuilder(SB_tic, -2, ow) #generate a new tau and ticket with foraging action, and add it to the timeline
    if new_tic=={}: 
        male_states[ow]=[t_max, -10, timeholder] #still need to show male is at bower, but -10 action is gibberish (since male won't leave bower before tmax)
    else: 
        if new_tic['action']==-7: #If the next action will be repair bower
            male_states[ow]=1 #A CHANGE: we don't know when male will leave bower but we need to state he is at bower now
        else:
            male_states[ow]=[new_tic['time'],new_tic['action'],timeholder]
            
            
            
#Foraging ticket handler. Ticket read, and male state changes to no longer at bower. Generates a stay at bower ticket.
def FGtickethandler(FG_tic):
    ow=FG_tic['owner'] 
    t=FG_tic['time']
    ta=FG_tic['tau']
    #print(male_states[ow])
    if t==0: #in this case male_states[ow]=0
        #male_states[ow]=0 #male is no longer at bower (this for if males start at SB)
        futurebuilder(FG_tic,-1,ow)   
    elif male_states[ow][0]!=t:
        discards.append(FG_tic)
        timeline[timeholder]['action']=abs(FG_tic['action']) 
    else:
        male_states[ow]=0 #male is no longer at bower
        futurebuilder(FG_tic, -1, ow)
        
#Maurad travel ticket handler. Male state changes to no longer at bower, and generates a maurad action ticket.
def MTtickethandler(MT_tic):
    ow=MT_tic['owner']
    targ=MT_tic['target']
    t=MT_tic['time']
    if male_states[ow][0]!=t:
        discards.append(MT_tic)
        timeline[timeholder]['action']=abs(MT_tic['action']) #A CHANGE
        print("malestates is {:f} while tictime is {:f}".format(male_states[ow][0], t))
    else:
        male_states[ow]=0 #male is no longer at his bower
        futurebuilder(MT_tic, -5, targ)

#Maurad action ticket handler. The bower destruction occurs if the targeted bower's owner is absent and the bower is intact. 
#Otherwise, the tau for this ticket is zero (bird immediately turns around). This ticket handler then generates a
#maurad return ticket.
def MAtickethandler(MA_tic):
    targ=MA_tic['target']
    if male_states[targ]==0 and bower_states[targ]==1: #if the bower is intact and its owner is absent
        bower_states[targ]=0
    else: #in all other cases bowerbird immediately leaves
        MA_tic['tau']=0 #COMMENT! Changing tau for this ticket as we read it bc stay is cut short by bower owner's presence
    futurebuilder(MA_tic, -6, targ)


#Repair bower / maurad return ticket handler. This ticket handler then generates a ticket for stay at bower.
def RBMRtickethandler(RBMR_tic):
    ow=RBMR_tic['owner']
    futurebuilder(RBMR_tic, -1, ow)

       
    
#Female visitation ticket handler. Females visit and mate with males if the following conditions are met: 
#(1) The male is at the bower, (2) the bower is intact, and (3) no other female is present.
#If not,the female keeps this male on her recents list, and travels to additional males with probabilities based on a preference matrix,
#If the female finds no eligeble males but her recents list is full, a longer tau is generated. 
#Her short term memory is cleared (the recents list), and she can try any of the males again. This continues 
#until she mates succusfully. Then, the male tickets for stay at bower are extended until the female leaves. 
def FVtickethandler(FV_tic, recents_list):
    targ=FV_tic['target']
    ow=FV_tic['owner']
    t=FV_tic['time']
    recents_list=d["rl{0}".format(ow)]
    r=random.random() #generate this to decide whether mating happens if other conditions are met
    if bower_states[targ]==1 and male_states[targ]!=0 and r<success_rate and t>mating_states[targ]: #if the bower is intact and the male is present
        tau_court= 0.25 #numpy.random.normal(loc=.1504, scale=.0102, size=1)[0]
        timeline[timeholder]['tau']=tau_court #if mating is successful, then it takes .25hrs
        t_court_end=t+tau_court
        mating_states[targ]=t_court_end
        fitness_states[targ]=fitness_states[targ]+1 #assumption: female always mates if bower is intact and male present
        success_times.append(t_court_end) #this is the time at which the mating finishes (not starts, tho it could be)       
        if male_states[targ][0]<t_court_end:
            SB_tic=timeline[male_states[targ][2]] #this SB ticket has the wrong tau -- we must modify the timeline
            SB_tic['tau']=t_court_end-male_states[targ][0]+SB_tic['tau'] #the new tau is generated by tacking on the extension of SB due to FV
            timeline[male_states[targ][2]]['tau']=SB_tic['tau'] #modify the ticket on the timeline itself
            if male_states[targ][1]==-4: #if a MT ticket, generate a new tau and new_targ (individual to be marauded by targ)
                new_targ=numpy.random.choice(list(range(nodes)), p=visit_preferences[targ]) #choosing the male to maurad based on visit preferences
            else: #if a FG ticket, generate a new tau and set new_targ to targ
                new_targ=targ #targ=ow (or in this case new_targ=targ) when it's an FG_tic
            futurebuilder(SB_tic, male_states[targ][1], new_targ)
            male_states[targ][0]=t_court_end #now change male states so that the leave_time is accurate 
    else: #if female does not successfully mate
        #HEY!!: tau is court time not time until next FV... consider changing to use futurebuilder
        recents_list.append(targ)
        if len(recents_list)==min(max_visits, nodes): #if she's already visited her max # of males and not mated, reset recents and use nexttau
            recents_list=[]
            new_FV_targ=numpy.random.choice(list(range(nodes)))
            new_FV_time=t+numpy.random.uniform(FV_param[0], FV_param[1]) #she goes to another male after waiting some time (nexttau), courting takes no time
            if new_FV_time<t_max:
                new_FV_tic=ticketgenerator(0,new_FV_time, ow, -3, new_FV_targ, t)
                addtotimeline(new_FV_tic)
        else: #otherwise find a male not in recents and use travel_times
            new_FV_targ=-1 #just so that the code goes into the while loop the first iteration
            while(new_FV_targ in recents_list or new_FV_targ==-1):
                new_FV_targ=numpy.random.choice(list(range(nodes)), p=visit_preferences[targ]) #choose a male based on preference (a function of distance)
            new_FV_time=t+travel_times[targ][new_FV_targ] #she goes directly to this male
            if new_FV_time<t_max:
                new_FV_tic=ticketgenerator(0,new_FV_time, ow, -3, new_FV_targ, t)
                addtotimeline(new_FV_tic)
    return recents_list
