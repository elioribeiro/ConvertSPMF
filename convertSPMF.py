import pm4py
import pandas as pd
import numpy as np


#This function will convert the file to the format used by the SPMF tool
def convertSPMF(path,outputFileName):
    ocel = pm4py.read_ocel(path)

    ocel.events['ocel:activity'] = ocel.events['ocel:activity'].str.replace(' ', '')
    eventList = ocel.events["ocel:activity"].unique()

    df = pd.read_csv('temp/graphs.csv',sep=',')

    ocel.relations['ocel:activity'] = ocel.relations['ocel:activity'].str.replace(' ', '')

    file = open("temp/"+outputFileName+".txt", 'w+')
    file.writelines(u'@CONVERTED_FROM_TEXT'+"\n")

    activityToIndex = {activity: idx + 1 for idx, activity in enumerate(eventList)}
    for i in range(len(eventList)):
        file.write('@ITEM='+str(i+1)+"="+eventList[i].replace(' ','')+"\n")
    file.write('@ITEM=-1=|'+"\n")

    index = 0
    for i, row in df.iterrows():
        list = set(row[0].split())

        while index < len(ocel.relations) and ocel.relations.iloc[index, 3] in list:

            if ocel.relations.iloc[index, 0] != ocel.relations.iloc[index - 1, 0]:
                activity = ocel.relations.iloc[index, 1]
                activity_index = activityToIndex[activity]
                file.write(f'{activity_index} -1 ')
            index += 1

        file.write('-2\n')

    file.close()