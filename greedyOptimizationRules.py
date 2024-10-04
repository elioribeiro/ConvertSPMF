#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import time

import pandas as pd

import os
import csv


# In[ ]:


#This function is used to read a CSV file independent of the delimiter of the file
def read_csv_with_auto_delimiter(file_name):
    # Open the file and use csv.Sniffer to detect the delimiter
    with open(file_name, 'r') as file:
        sample = file.read(4096)
        dialect = csv.Sniffer().sniff(sample)
        file.seek(0)
        # Read the CSV file with the detected delimiter
        df = pd.read_csv(file, delimiter=dialect.delimiter)
    return df


# In[ ]:


#indicate the number of cluster (-1 is not to save cluster number)
K="-1"#"10"


Col_goal=""#"O_Refused" # whether to filter on consequent by specific value
Col_Sort="Lift(A=>B)"
Col2_Sort="Chi-square"#"Lift(A=>B)"

Mesure="Lift(A=>B)"#"Sup(A=>B)"

numcluster=int(K)

#filename is input file name with the initial set of rules (filtered rules)
filename=".\\TEST\\supoprtNTest-WithFilterComplexRules.csv"

#filenamesave is the output file name with the reduced set of rules
filenamesave = os.path.splitext(filename)[0]+"-Optimized.csv"

print(filename)
print(filenamesave)

#df=pd.read_csv(filename,delimiter=",")

df = read_csv_with_auto_delimiter(filename)


# In[ ]:


print(df)


# In[ ]:


df2=df.copy()

if Col_goal!="":    
    
    df2 = df[df['consequents'] == Col_goal].reset_index(drop=True)


# In[ ]:


df2 = df2.sort_values([Col_Sort,Col2_Sort], ascending=False)


# In[ ]:


antecedents=df2["antecedents"]


# In[ ]:


list_antecedents=[]

for a in antecedents:
    parts=a.split("-")
    print(parts)
    
    for p in parts:
        if p not in list_antecedents:
            list_antecedents.append(p)

print("Numb. of different items in antecedent=",len(list_antecedents))
print("Items=",list_antecedents)


# Greedy function that returns which rules in df2 maximize the chosen measure (Lift(A=>B)) and have the largest possible number of items in the antecedents (list_antecedents)

# In[ ]:


def greedy(df3,mesure,list_antecedents):
    #value of the sum of the chosen rules measure
    fo=0 
    #lista das regras selecionadas
    list_regras=[]
    #list of selected rules
    list_numregras=[]
    
    #list of antecedents already obtained
    list_ant=[]
    
    for i in range(len(df3)):        
        #get the rule background
        parts=df3.iloc[i]["antecedents"].split("-")
                       
        #says he didn't catch any
        pegou=False
        for p in parts:
               
            if p not in list_ant:
                list_ant.append(p)
                #got any antecedent
                pegou=True
                
        if pegou:
            fo=fo+df3.iloc[i][mesure]
            list_regras.append(df3.iloc[i])
            list_numregras.append(i)
        
        if len(list_ant)==len(list_antecedents):
            print("list_ant=",list_ant)
            print("list_antecedents=",list_antecedents)
            
            #conclude the solution
            break
            
    return fo, list_regras, list_numregras            


# In[ ]:


fo,list_regras,list_numregras=greedy(df2,Mesure,list_antecedents)

print("Simple Greedy Method")
print("Sum of Mesures of the Chosen Rules=",fo)
print("Number of Chosen Rules(",len(list_numregras),")",list_numregras)
print("Chosen Rules")
for i in list_regras:
    print(i)
    print("------------")


# In[ ]:


def greedy2(df3,mesure,list_antecedents,num):
    
    df4=df3.copy()
    
    #value of the sum of the measure of the chosen rules
    fo=0 
    
    #list of selected rules
    list_regras=[]
    #list of selected rule numbers
    list_numregras=[]
    
    #list of antecedents already obtained
    list_ant=[]
    
    for i in range(len(df4)):
        
        select=[]
        #f=i+num
        f=num
        if f>len(df4):
            f=len(df4)
        
        #select = [x for x in range(i, f)]
        select = [x for x in range(0, f)]
                
        k = random.choice(select)
        
        
        #get the rule background
        parts=df4.iloc[k]["antecedents"].split("-")
                
        
        get=False
        for p in parts:
            if p not in list_ant:
                list_ant.append(p)
                
                pegou=True
                
        if pegou:
            fo=fo+df4.iloc[k][mesure]
            list_regras.append(df4.iloc[k])
            list_numregras.append(df4.iloc[k].name)        
        
        if len(list_ant)==len(list_antecedents):
           
            break
            
        k_name=df4.iloc[k].name
        df4 = df4.drop(k_name)
        continue
            
    return fo, list_regras, list_numregras


# Iterative Greedy Method 

# In[ ]:


def mult_greedy(rep,df3,mesure,list_antecedents,num):
    best=0#99999999999
    best_list_rules=[]
    best_list_numrules=[]
    for i in range(rep):
        
        random.seed(time.time())
        
        fo,list_rules,list_numrules=greedy2(df3,mesure,list_antecedents,num)
        
        if fo > best:
            best=fo
            best_list_rules=list_rules
            best_list_numrules=list_numrules
            
    return best, best_list_rules, best_list_numrules


# In[ ]:


Max_Iter=1000 #Max number of iterations 
best, best_list_rules, best_list_numrules=mult_greedy(Max_Iter,df2,Mesure,list_antecedents,3)

print("Sum of Chosen Rule Measurements=",best)
print("Number of Rules Chosen(",len(best_list_numrules),")",best_list_numrules)
print("Chosen Rules")
for i in best_list_rules:
    print("Antecedent=",i["antecedents"])
    print("Consequent=",i["consequents"])
    print("Lift(A=>B)=",i["Lift(A=>B)"])
    
    print("Sup(A=>B)",i["Sup(A=>B)"])
    print("Conf(A=>B)=",i["Conf(A=>B)"])
    print("------------")


# In[ ]:


def save_list_to_file(filename, list_to_save):
    with open(filename, 'w') as f:
        cont=1
        
        f.write("#Rule,Antecedent,Consequent,Lift(A=>B),Sup(A=>B),Conf(A=>B),Cluster\n")
        for i in list_to_save:
            
            f.write("Rule %s" % cont)
            f.write(",%s" % i["antecedents"])
            f.write(",%s" % i["consequents"])
            f.write(",%s" % i["Lift(A=>B)"])
            f.write(",%s" % i["Sup(A=>B)"])
            f.write(",%s" % i["Conf(A=>B)"])
            if numcluster!=-1:
                f.write(",%s\n" % numcluster)
            else:
                f.write("\n")
            
            cont=cont+1


# In[ ]:


print(best_list_rules)


# In[ ]:


#saves the file with the final rules selected
save_list_to_file(filenamesave, best_list_rules)


# In[ ]:




