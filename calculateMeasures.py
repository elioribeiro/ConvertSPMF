import pandas as pd
from util import transactionCount, calculateSupport

def calculateMeasures(SPMFInputPath,SPMFOutputPath):
    path = SPMFInputPath
    df = pd.read_csv(SPMFOutputPath,delimiter=' ',header=None)



    df[4] = df[4] / transactionCount(path)
    listA = df[0].tolist()
    listB = df[2].tolist()

    print(transactionCount(path))

    df[0] = df[0].str.replace(',', '-')
    df[2] = df[2].str.replace(',', '-')

    supportListA = calculateSupport(listA,path)
    df['Sup(A)'] = supportListA

    supportListB = calculateSupport(listB,path)
    df['Sup(B)'] = supportListB

    df['Lift(A=>B)'] = round(df[6] / df['Sup(B)'], 4)

    df['Chi-square'] = round(((df[4] - df['Sup(A)'] * df['Sup(B)']) ** 2 * transactionCount(path)) / (
                        df['Sup(A)'] * (1 - df['Sup(A)']) * df['Sup(B)'] * (1 - df['Sup(B)'])), 4)



    df.rename(columns={0: 'antecedent'}, inplace=True)
    df.rename(columns={1: '=>'}, inplace=True)
    df.rename(columns={2: 'consequent'}, inplace=True)

    df['Sup(A=>B)'] = df[4]
    df['Conf(A=>B)'] = df[6]

    removeColumns = [3, 4, 5, 6]
    df = df.drop(removeColumns, axis=1)



    newColumnOrder = ['antecedent  ', '=>', 'consequent', 'Sup(A)', 'Sup(B)', 'Sup(A=>B)', 'Conf(A=>B)',
                                  'Lift(A=>B)', 'Chi-square']
    df = df[newColumnOrder]

    df.to_csv("temp/outputRulesWithMetrics"+".csv", sep=',', index=False)
