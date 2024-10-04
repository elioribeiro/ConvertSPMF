#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
import csv
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


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


#Whether to filter complex rules or not
DOFILTER=True#False

#Whether to filter some Activities of Antecedents
DOFILTER2=False#True

#Whether will use the lift as a filter (FILTER D)
DOFILTER3=True

#Whether will use the chi-square statistical test (FILTER C)
DOFILTER4=True

#Whether will filter by a specific consequent (FILTER B)
DOFILTER5=False#True#False

#Specific consequent to FILTER B
goal="O_Refused"

#Do something if have suporteitem file
HAVESUPPORTITEM=False


#Reads the basic CSV dataset

#filename is input file name with the initial set of rules
filename=".\\TEST\\supoprtNTest.csv"

#filenamesave is the output file name with the reduced set of rules
filenamesave = os.path.splitext(filename)[0]

print(filename)
print(filenamesave)

df = read_csv_with_auto_delimiter(filename)

#create two new columns with the antecedents and consequents as string separated by space
df['antecedents2'] = df['antecedents'].apply(lambda x: ' '.join(x.split('-')))
df['consequents2'] = df['consequents'].apply(lambda x: ' '.join(x.split('-')))

print("Initial Size of the dataset=",len(df))


# In[ ]:


if DOFILTER2:
    df = df[~df['antecedents'].str.contains("A_Denied")]
    display(df)


# In[ ]:


dfx=df.copy()

#FILTER D
if DOFILTER3:
    # Filter rules by lift greater than 1
    df = df[df['Lift(A=>B)'] > 1]    
    
    if len(df)==0:
        df=dfx.copy()


# In[ ]:


from scipy.stats import chi2
import statsmodels.stats.multitest as smt

#FILTER C
if DOFILTER4:
    dof=1
    
    df = df.dropna(subset=['Chi-square'])

    df['p-value']=df['Chi-square'].apply(lambda x: chi2.sf(x, dof))


    # Assuming 'p-value' is the column with the original p-values
    pvals = df['p-value'].values
    #reject, pvals_corrected, _, _ = smt.multipletests(pvals, method='fdr_bh')
    reject, pvals_corrected, _, _ = smt.multipletests(pvals, method='bonferroni')

    # Adding the corrected p-values as a new column to the DataFrame
    df['p-value-cor'] = pvals_corrected
   


# In[ ]:


df2=df

#filter the rules that have consequent as O_Refused
if DOFILTER5:
    df2 = df2[df2['consequents'] == goal].reset_index(drop=True)

tam_all=len(df2)


# In[ ]:


# FILTER C
if DOFILTER4:
    # Filter rules by p-value-cor lower than alpha
    alpha=0.05 #critical value    
    df2 = df2[df2['p-value-cor'] < alpha]

    print("Number of Final Rules=",len(df2))


# In[ ]:


filtered_rules=df2


# In[ ]:


# Filter out redundant rules
nonr_rules = filtered_rules.drop_duplicates(subset=['antecedents2', 'consequents2'])

print("Number of Rules=",len(nonr_rules))


# In[ ]:


# Identify redundant rules based on the lift measure
def is_redundant(rule, nonr_rules):
    """
    Check if a rule is redundant. A rule is redundant if there exists another rule
    with the same consequent and a subset of the antecedent with a higher or equal lift.
    """
    antecedents = rule['antecedents3']
    consequents = rule['consequents']
    lift = rule['Lift(A=>B)']

    for _, candidate_rule in nonr_rules.iterrows():
        if candidate_rule['consequents'] == consequents:
            #if antecedents.issuperset(candidate_rule['antecedents']) and candidate_rule['lift'] >= lift:#>= lift:
            if candidate_rule['antecedents3'].issuperset(antecedents) and candidate_rule['Lift(A=>B)'] < lift:#>= lift:
                return True
    return False

if DOFILTER:
    # Filter out redundant rules
    # Assuming 'nonr_rules' is your dataframe and 'antecedents2' is the column with space-separated strings
    nonr_rules['antecedents3'] = nonr_rules['antecedents2'].apply(lambda x: set(x.split()))
    nonr_rules = nonr_rules[~nonr_rules.apply(lambda rule: is_redundant(rule, nonr_rules), axis=1)]


# In[ ]:


if HAVESUPPORTITEM:
    df5=pd.read_csv("SuporteItem.txt")
    display(df5)
    print(df5.columns)


# In[ ]:


if HAVESUPPORTITEM:
    antecedents=nonr_rules["antecedents"]

    list_items=[]

    for ant in antecedents:
    
        str_itens=""
    
        itens=ant.split("-")
    
        for it in itens:
            sup=df5[df5['Item'] == it]['Sup'].iloc[0]
            str_itens=str_itens+it+"("+str(round(sup,6))+")-"
        
        list_items.append(str_itens)

    nonr_rules["antecedents"]=list_items

    display(nonr_rules)


# In[ ]:


# Save DataFrame to CSV
if DOFILTER:
    filenamesave=filenamesave+"-WithFilterComplexRules.csv"
    nonr_rules.to_csv(filenamesave, index=False)
else:
    filenamesave=filenamesave+"-NoFilterComplexRules.csv"
    nonr_rules.to_csv(filenamesave, index=False)


# In[ ]:




