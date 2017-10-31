# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 11:23:41 2017

@author: Qi
"""

"""
following are the field of interest and positions-starts from 1
CMTE_ID(1): identifies the flier, which for our purposes is the recipient of this contribution
ZIP_CODE(11): zip code of the contributor (we only want the first five digits/characters)
TRANSACTION_DT(14): date of the transaction
TRANSACTION_AMT(15): amount of the transaction
OTHER_ID(16): a field that denotes whether contribution came from a person or an entity


CMTE_ID(0):
ZIP_CODE(10):
TRANSACTION_DT(13): 
TRANSACTION_AMT(14):
OTHER_ID(15):


1.open file
2.read file line by line
3.each line is read as a string, split string by delimiter '|'
4.index element in the list, use position-1 as the index for the element of interest
5.check CMTE_ID and TRANSACTION_AMT, ignore null
6.check TRANSACTION_DT, if invalid still output to medianvals_by_zip but not medianvals_by_date
7.check ZIP_CODE, if invalid still output to medianvals_by_date, but not medianvals_by_zip
8.write to zip_file line by line
9.sort list and then write to date_file 
"""
import os
#look for the input file by using the structure of the folder and path of .py file
dirname = os.path.dirname
parentpath =dirname(os.path.abspath("political_donors_stats.py"))
#print parentpath
#noticed a difference in between running in local IDE and in shell, the following line is to locate the correct directory 
if(parentpath[-3:] == 'src'): 
    parentpath = dirname(parentpath)

#write output file    
zip_file = open(parentpath+"\\output\\medianvals_by_zip.txt",'w')
dt_file = open(parentpath+"\\output\\medianvals_by_date.txt",'w')

#create two dictionaries for storing information for two output files

stats_zip = {} # structure is {CMTE_ID|ZIP_CODE}:[appearance, [all appeared TRANSACTION_AMT]]
stats_dt ={} #structure is {CMTE_ID:{TRANSACTION_DT: [TRANSACTION_AMT]}}

print "Start reading data"
#breaker = 0  # use breaker for testing with large file
with open(parentpath+"\\input\\itcont.txt") as itcont:
    for line in itcont:
#        breaker+= 1
#        if breaker ==1000:
#            break
        line_split = line.split('|')
        if (line_split[0]!='' and line_split[14]!='' and line_split[15]==''):
            if (len(line_split[10])==9): #valid zipcode
                if (line_split[0]+'|'+line_split[10][0:5] not in stats_zip):
                   stats_zip[line_split[0]+'|'+line_split[10][0:5]] = [1 , [int(line_split[14])]] #first appearance: create a new entry in dictionary
                   zip_file.write(line_split[0]+'|'+line_split[10][0:5]+'|'+line_split[14]+'|'+'1'+'|'+line_split[14]+'\n')
                else:
                   stats_zip[line_split[0]+'|'+line_split[10][0:5]][0]+=1 #if now new- running num +1
                   running_num = stats_zip[line_split[0]+'|'+line_split[10][0:5]][0]
                   stats_zip[line_split[0]+'|'+line_split[10][0:5]][1].append(int(line_split[14])) #append new trasaction amout
                   stats_zip[line_split[0]+'|'+line_split[10][0:5]][1].sort() #sort this list for calculating median
                   if (running_num%2 ==1): #since list is sorted, if total number is odd, take the one in the middle
                      running_median = stats_zip[line_split[0]+'|'+line_split[10][0:5]][1][(running_num - 1)/2]
                   else:# if even number in the list, take the average of middle 2 numbers
                      running_median = int(round((stats_zip[line_split[0]+'|'+line_split[10][0:5]][1][running_num /2 -1]+ stats_zip[line_split[0]+'|'+line_split[10][0:5]][1][running_num/2])/2.)) #take mean then round                 
                   running_sum = sum( stats_zip[line_split[0]+'|'+line_split[10][0:5]][1])
                   zip_file.write(line_split[0]+'|'+line_split[10][0:5]+'|'+str(running_median)+'|'+str(running_num)+'|'+str(running_sum)+'\n') # _zip.txt is written when data is streaming in
            if (len(line_split[13]) == 8):#valid date is mmddyyyy
                month = int(line_split[13][0:2])
                date = int(line_split[13][2:4])
                year = int(line_split[13][4:8])
                if(0<date<32 and 0<month<13 and 1700< year < 2018): #if date is valid,  create nested dictionary for sorting
                    if(line_split[0] not in stats_dt): 
                        stats_dt[line_split[0]] = {} # first layer of dictionary, key is ID
                        stats_dt[line_split[0]][line_split[13]] = [1, [int(line_split[14])],year*10000+month*100+date]# second layer, key is date, data is [total number, list of transactions, running_median, running_total amount, date as a number]                   
                    elif (line_split[0] in stats_dt and line_split[13] not in stats_dt[line_split[0]] ):
                        stats_dt[line_split[0]][line_split[13]] = [1, [int(line_split[14])],year*10000+month*100+date]                           
                    else:
                        stats_dt[line_split[0]][line_split[13]][0]+= 1
                        stats_dt[line_split[0]][line_split[13]][1].append(int(line_split[14]))
                        stats_dt[line_split[0]][line_split[13]][1].sort()
            
for ID in sorted(stats_dt.keys()): #sort by ID
    for line_dt in sorted(stats_dt[ID].items(),  key= lambda x:x[1][2]): #sort by the date, by using a number year*10000+month*100+date
        total_num_dt = line_dt[1][0]
        if (total_num_dt % 2 == 1):
            median_dt = line_dt[1][1][(total_num_dt - 1)/2]
        else:
            median_dt = int(round((line_dt[1][1][total_num_dt /2 - 1] + line_dt[1][1][total_num_dt/2])/2.))
        sum_dt = sum(line_dt[1][1])            
        dt_file.write(ID+'|'+line_dt[0]+'|'+str(median_dt)+'|'+str(total_num_dt)+'|'+str(sum_dt)+'\n')

print "output file finished, please check in the"+ '"output"'+"folder"
itcont.close()
zip_file.close()
dt_file.close()    
