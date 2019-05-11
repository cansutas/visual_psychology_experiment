
#==============================================================================
# Specify the stimulus folder and import the stuff
#==============================================================================
import os
import random
from psychopy import visual, event, core
import time

dire = #directory of the Project file
os.chdir(dire)

from funcfile import dialogbox, writetocsv


#==============================================================================
# Create filepath lists for living and non-living and datafolder for CSV writer
#==============================================================================
livinglist = os.listdir(dire + str("/stimuli/Living"))
nonlivinglist = os.listdir(dire + str("/stimuli/NonLiving"))
datapath=dire+str("/data/") #Datapath for CSV writer


#==============================================================================
# Randomize the lists
#==============================================================================
random.shuffle(livinglist)
random.shuffle(nonlivinglist)

#==============================================================================
# #============================================================================
# --------------------------VISUAL PART----------------------------------------
#----------------From here on, run everything together or it will crash--------
#==============================================================================
 
my_window=visual.Window(size=(1000,600), units = 'pix', color='black')

#==============================================================================
# Fill lists with picture objects
#==============================================================================
livinglistpic=list([])  #List for living picture objects
nonlivinglistpic=list([])   #List for non-living picture objects
for i in range(0,20):
    livinglistpic.append(visual.ImageStim(my_window, image=dire + str("/stimuli/Living/")+ livinglist[i]))
    nonlivinglistpic.append(visual.ImageStim(my_window, image=dire + str("/stimuli/Nonliving/")+ nonlivinglist[i]))

#The introtext and endtext
intro="You will be presented with two images in succession. Press L if the second picture is a living object. Press A if it is a non-living object. Press space bar to start."
end="Thank you for your participation. Window will close now. "

#Create text elements
introtext=visual.TextStim(my_window, text=intro, font='arial', height=20, bold=True)  #Intro text
endtext=visual.TextStim(my_window, text=end, font='arial', height=20, bold=True)  #End text
cross=visual.TextStim(my_window, text='+', font='arial', height=20, bold=True)  #Screen cross


#==============================================================================
# Initialize
#==============================================================================
rnd=random.sample(range(0, 20), 20)  #Responsible for the random numbers the condition if statements are based on
start_time=0  #The variable for the start time for the reactiontime measurement
end_time=0  #The variable for the end time for the reactiontime measurement
primetime=0.2    #Length of prime presentation
targettime=1.5    #Length of target presentation
timetorespond=3   #Time to respond
rt=0 #The variable the reaction time will be stored in

prime = [1] * 5 + [0] * 10 + [1] * 5 
target = [1] * 5 + [0] * 5 + [1] * 5 + [0] * 5

L_num=0 #The living picture index
NL_num=0 #The non-living picture index

keypresslist=list() #List for keypresses
reactiontimelist=list() #List for reaction times
orderprime=list()   #List that saves the order of the primes for output file
ordertarget=list()  #List that saves the order of the targets for output file
triallist=range(1,21) #Trial numbers for output file


#==============================================================================
# Display code
#==============================================================================

trial_clock=core.Clock()
trial_clock.reset()   
clock_running=True 
intro=True  #Keeps the introtext in a loop till spacebar is pressed
ending=False #Keeps the endtext in a loop till time expires
participantnumber = dialogbox() #Call the function dialogbox for participant number
# SHOW INTRODUCTION TEXT
while intro==True:  #The intro loop
    introtext.draw()
    my_window.flip()
    if event.getKeys(['space']): #Continue experiment on space
        intro=False
        break
# ITERATE OVER EXPERIMENTAL TRIALS   
for i in rnd:
    orderprime.append(prime[i]) #Add prime order information to list
    ordertarget.append(target[i]) #Add target order information to list
    response=False
    if event.getKeys(['escape']):  #Close window on escape press
        clock_running=False
        my_window.close()
   # DRAW PRIME STIMULUS
    if prime[i]==1:  
        livinglistpic[L_num].draw()   #Draw living stimulus from the list based on the indexing variable
        L_num+=1
    else:
        nonlivinglistpic[NL_num].draw()     #Draw non-living stimulus from the list based on the indexing variable   
        NL_num+=1  
    my_window.flip()
    core.wait(primetime)# Wait time
    event.clearEvents() #Clear input buffer
     # DRAW TARGET STIMULUS AND WAIT FOR A RESPONSE
    if target[i]==1:  
        targetpic=livinglistpic[L_num] #Save target picture to temporary variable
        L_num+=1
    else:
        targetpic=nonlivinglistpic[NL_num]  #Save target picture to temporary variable   
        NL_num+=1  
    start_time=trial_clock.getTime() #The start time for the reaction time measurement
    timeout = time.time() + timetorespond   #The time to respond that breaks the loop eventually
    targetlooptime=time.time() + targettime #The timer that first presents the target stimulus and then the cross
    while True:
        if time.time() < targetlooptime: #Present the target for the required duration
            targetpic.draw()
            my_window.flip() 
        if time.time() > targetlooptime: #Presents the cross for the required duration
            cross.draw()
            my_window.flip() 
        if event.getKeys(['a']) and response==False:    #A represents NON-LIVING
            end_time=trial_clock.getTime()
            rt=end_time-start_time
            reactiontimelist.append(rt)  #Add reaction time to list
            keypresslist.append("a") #Add response to list
            response=True
        if event.getKeys(['l']) and response==False:    #L represents LIVING
            end_time=trial_clock.getTime()
            rt= end_time-start_time
            reactiontimelist.append(rt)  #Add reaction time to list
            keypresslist.append("l") #Add response to list
            response=True
        if time.time() > timeout: #Breaks the loop after the response time expired
            break  
    if response==False:
        reactiontimelist.append('NaN')  #Add NaN (no response) to list when no response in time
        keypresslist.append('NaN') #Add NaN (no response) to list when no response in time
    if L_num==20 and NL_num==20: #Breaks the main loop after all target and prime stimuli have passed
        ending=True
        break

# SHOW THE END OF THE EXPERIMENT
while ending==True:
    endtext.draw()
    my_window.flip()
    core.wait(2)
    my_window.close()
    writetocsv(datapath,participantnumber,triallist, orderprime, ordertarget, reactiontimelist, keypresslist) #Write the data to an output file





