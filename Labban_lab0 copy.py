#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import math


# In[2]:


#Question 1
#the main list
mylist = ['roads', 'cities', 'counties', 'states']
print(mylist)

#the empty list
newlist = []
print(newlist)

#the concatenating of the strings above with .txt
for x in mylist:
    newlist.append(x + '.txt')

#final result!
print(newlist)


# In[3]:


#Question 2
#the set up of the numbers
exponent = 0
num = math.pi
#the loop with the results outputting
while num ** exponent < 10000:
    print (num ** exponent)
    exponent += 1
#answer to the question; What condition are you testing?
#The condition that is being tested is to run pi raised to a power,
#starting at 0, coninuing until the value would reach 10000 or higher.
#This was only able to go up to pi to the power of 8. 
#Ultimetly the conditon tested used the while function to see what 
#exponent pi raised to in order to reach the limit set (<10000) for 
#pi being raised to a power (exponent) within the set limit, stopping 
#right before it reaches that threshhold/ boundry

