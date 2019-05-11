# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 18:35:53 2016

@author: Hanker
"""

#==============================================================================
# Dialogue input box for participant number function
#==============================================================================

from Tkinter import * #If we dont do it like this we get:  NameError: global name 'Tk' is not defined
import csv


def dialogbox():    
    master = Tk()
    Label(master, text="Participant_Number").grid(row=0)
    w = StringVar()
    e1 = Entry(master, textvariable = w)
    e1.grid(row=0, column=1)
    Button(master, text='Ok', command=master.destroy).grid(row=3, column=1, sticky=W, pady=4)
    master.mainloop()
    return w.get()
    
    
#==============================================================================
# Write the data to a CSV file
#==============================================================================

def writetocsv(datapath,participantnumber,triallist, orderprime, ordertarget, reactiontimelist, keypresslist):
    rows=zip(triallist, orderprime, ordertarget, reactiontimelist, keypresslist)
    headings=('Trial', 'Prime', 'Target', 'RT', 'Response')
    rows.insert(0, headings)
    filename=datapath+participantnumber + str("_data.csv")
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
        
        
        
#==============================================================================
# Function to calculate correct answers for each condition
#==============================================================================

def correct_answers(data,prime, target, response): 
    #x is defined as the count of 'response' in conditions where prime is 'prime' and the target is 'target'    
    x= data[(data['Prime'] == prime ) & (data['Target'] == target) & (data['Response'] == response)].count()
    z= x['Response']
    return z    

    
    
