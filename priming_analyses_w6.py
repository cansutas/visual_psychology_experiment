# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 14:24:21 2016

@author: cansu
"""
import os
import pandas
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()

dire = 'C:/Users/LBP.P102PW036/Google Drive/KULeuven/Computer in Psychology/Project'
#dire = 'C:/Users/cansu/Google Drive/KULeuven/Computer in Psychology/stimuli'
os.chdir(dire)

from funcfile import correct_answers

#==============================================================
#-----------------Analyses-------------------------------------
#==============================================================

#------Creating the mean RT and correct answer values for each condition, over all participants--------

y=[]
RT_means=[]
CA_means=[]#correct answer means
correct_list=[]
condition_num=4 #number of conditions

#Read the data file
data_list= os.listdir(dire + str("/data"))

for i in data_list:
    filename= dire + str("/data/")+ i
    data = pandas.read_csv(filename, sep=',', na_values="NaN")
    #General descriptives to check the data
    print pandas.DataFrame.describe(data)    
    #Group the data based on the conditions    
    Conditions= data.groupby(['Prime', 'Target'])    
    #Print and save the mean RT for each condition in this order:
    #NL_congruent, L_incongruent, NL_incong, L_cong
    for conditi, value in Conditions['RT']:
        print((conditi, value.mean()))
        y.append(value.mean())
    #Saves the number of correct answer for each condition    
    correct_list.append(correct_answers(data,0,0, 'a')) #NL cong
    correct_list.append(correct_answers(data,1,0, 'a')) #NL incog
    correct_list.append(correct_answers(data,1,1, 'l')) #L cog
    correct_list.append(correct_answers(data,0,1, 'l')) #L incog
#Save the mean RT and the number of correct answers for each condition across participants
for n in range(0,condition_num):
    cond_RT_mean=np.mean(y[n::4]) #selects the n'th, n+4'th and n+8'th variables (the same condition for each person) 
    RT_means.append(cond_RT_mean) #takes the mean of those variables and saves
    cond_CA_mean=np.mean(correct_list[n::4])
    CA_means.append(cond_CA_mean)


#==============================================================
#-----------------The Plot for the Mean of RT------------------
#==============================================================

#Changing the indexing of variables to make the graphs more logical
RT_means[2], RT_means[1] = RT_means[1], RT_means[2] # now it is the means for NL_cong, Nl_incog, L_incog, L_cong
RT_means[3], RT_means[2] = RT_means[2], RT_means[3] # now it is  NL_cong, Nl_incog, L_cong L_incog
#Plot showing mean RT for each Condition
x=('NL_Cong', 'NL_Incong', 'L_Cong', 'L_Incong')
x_pos = np.arange(len(x)) #set the position of x axis variables
#Select and run from Start to End together
#Start
plt.bar(x_pos, RT_means, align='center', alpha=0.5) #create the bars, y is means of RT
plt.xticks(x_pos, x) #labeling of x axis bars
plt.ylabel('RT') #label of y axis
plt.title('Mean RT for each Condition')
plt.show()
#plt.savefig('RT_mean.png') #Use this if you want to save the figure
#End

#==============================================================================
#---The Plot for the Mean of the Number of Correct Answers for Each Condition--
#=============================================,================================

#Start
plt.bar(x_pos, CA_means, align='center', alpha=0.5) #create the bars, y is means of RT
plt.xticks(x_pos, x) #labeling of x axis bars
plt.ylabel('Correct Answers') #label of y axis
plt.title('Number of Correct Answers for each Condition')
plt.show()
#plt.savefig('Correct_answers.png') #Use this if you want to save the figure
#End


