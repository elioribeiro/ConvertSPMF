
import pandas as pd



def transactionCount(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    listWithoutAt = [line.strip().replace('-1', '').replace('-2', '') for line in lines if not line.startswith('@')]
    listWithoutAt = [line.split() for line in listWithoutAt]

    df = pd.DataFrame(listWithoutAt)

    quantity = df.shape[0]

    return quantity

def calculateSupport(myList,path):


    with open(path, 'r') as file:
        lines = file.readlines()

    valores_com_arroba = [line.strip().split('=')[2].replace('|', '') for line in lines if line.startswith('@ITEM')]


    listWithoutAt = [line.strip().replace('-1', '').replace('-2', '').split()
                        for line in lines if not line.startswith('@')]

    df = pd.DataFrame(listWithoutAt)


    mapping = {str(i + 1): valor for i, valor in enumerate(valores_com_arroba)}


    df = df.applymap(lambda x: mapping.get(x, x))


    supportList= []
    for items in myList:
        items = items.split(',')
        occurrences = df.apply(lambda row: all(item in row.values for item in items), axis=1).sum()
        supportList.append(occurrences / df.shape[0])

    return supportList


