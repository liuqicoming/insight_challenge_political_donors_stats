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
dirname = os.path.dirname
parentpath =dirname(os.path.abspath("political_donors_stats.py"))

zip_file = open(parentpath+"\\output\\medianvals_by_zip.txt",'w')
dt_file = open(parentpath+"\\output\\medianvals_by_date.txt",'w')

stats_zip = {} # this dictionary store CMTE_ID and ZIP_CODE as identifier and also TRANSACTION_AMT appeared so far
stats_dt ={}

print "Start reading data"
breaker = 0
with open(parentpath+"\\input\\itcont.txt") as itcont:
    for line in itcont:
        breaker+= 1
        if breaker ==1000:
            break
        line_split = line.split('|')
        if (line_split[0]!='' and line_split[14]!='' and line_split[15]==''):
            if (len(line_split[10])==9): #valid zipcode
                if (line_split[0]+'|'+line_split[10][0:5] not in stats_zip):
                   stats_zip[line_split[0]+'|'+line_split[10][0:5]] = [1 , [int(line_split[14])]] #first appear create a new entry in dictionary
                   zip_file.write(line_split[0]+'|'+line_split[10][0:5]+'|'+line_split[14]+'|'+'1'+'|'+line_split[14]+'\n')
                else:
                   stats_zip[line_split[0]+'|'+line_split[10][0:5]][0]+=1
                   running_num = stats_zip[line_split[0]+'|'+line_split[10][0:5]][0]
                   stats_zip[line_split[0]+'|'+line_split[10][0:5]][1].append(int(line_split[14])) 
                   if (running_num%2 ==1):
                      running_median = stats_zip[line_split[0]+'|'+line_split[10][0:5]][1][(running_num - 1)/2]
                   else:
                      running_median = int(round((stats_zip[line_split[0]+'|'+line_split[10][0:5]][1][running_num /2 -1]+ stats_zip[line_split[0]+'|'+line_split[10][0:5]][1][running_num/2])/2.)) #need float                 
                   running_sum = sum( stats_zip[line_split[0]+'|'+line_split[10][0:5]][1])
                   zip_file.write(line_split[0]+'|'+line_split[10][0:5]+'|'+str(running_median)+'|'+str(running_num)+'|'+str(running_sum)+'\n')
            if (len(line_split[13]) == 8):
                month = int(line_split[13][0:2])
                date = int(line_split[13][2:4])
                year = int(line_split[13][4:8])
                if(0<date<32 and 0<month<13 and 1700< year < 2018): # create nested dictionary for sorting
                    if(line_split[0] not in stats_dt):
                        stats_dt[line_split[0]] = {}
                        stats_dt[line_split[0]][line_split[13]] = [1, [int(line_split[14])], int(line_split[14]), int(line_split[14]),year*10000+month*100+date]
                    elif (line_split[0] in stats_dt and line_split[13] not in stats_dt[line_split[0]] ):
                        stats_dt[line_split[0]][line_split[13]] = [1, [int(line_split[14])], int(line_split[14]), int(line_split[14]),year*10000+month*100+date]                           
                    else:
                       stats_dt[line_split[0]][line_split[13]][0]+= 1
                       running_num_dt = stats_dt[line_split[0]][line_split[13]][0]
                       stats_dt[line_split[0]][line_split[13]][1].append(int(line_split[14]))
                       if (running_num_dt % 2 == 1):
                           running_median_dt = stats_dt[line_split[0]][line_split[13]][1][(running_num_dt - 1)/2]
                       else:
                           running_median_dt =int(round((stats_dt[line_split[0]][line_split[13]][1][running_num_dt /2 - 1] + stats_dt[line_split[0]][line_split[13]][1][running_num_dt/2])/2.))
                       running_sum_dt = sum(stats_dt[line_split[0]][line_split[13]][1])
                       stats_dt[line_split[0]][line_split[13]][2] = running_median_dt
                       stats_dt[line_split[0]][line_split[13]][3] = running_sum_dt
            
for ID in sorted(stats_dt.keys()):
    for line_dt in sorted(stats_dt[ID].items(),  key= lambda x:x[1][4]):
        dt_file.write(ID+'|'+line_dt[0]+'|'+str(line_dt[1][2])+'|'+str(line_dt[1][0])+'|'+str(line_dt[1][3])+'\n')

print "output file finished, please check in the"+ '"output"'+"folder"
itcont.close()
zip_file.close()
dt_file.close()    
