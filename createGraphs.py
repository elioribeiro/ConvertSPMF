import pm4py
from pm4py.algo.transformation.ocel.graphs import object_interaction_graph
from pm4py.algo.transformation.ocel.features.objects import algorithm
import networkx as nx
import pandas as pd

def createGraphs(path):

    ocel = pm4py.read_ocel(path)

    #Performs the creation of subgraphs and the extraction of features for each object
    graph = object_interaction_graph.apply(ocel)
    vertexList = list(ocel.objects[ocel.object_id_column])
    G = nx.Graph()
    graph = list(graph)
    for i in vertexList:
        G.add_node(i)
    for i in range(len(graph)):
        temp = graph[i]
        a = temp[0]
        b = temp[1]
        G.add_edge(a, b)
    subgraphs = [G.subgraph(s) for s in nx.connected_components(G)]
    data, feature_names = algorithm.apply(ocel)
    df_representation = pd.DataFrame(data,columns=feature_names)




    #Creating the DataFrame
    feature_names_final= ['@@object']
    df_representation_final = pd.DataFrame(columns=feature_names_final)



    #Groups the objects into their respective graphs and sums their features.
    for i in range(len(subgraphs)):
        tempFilter = pd.DataFrame(columns=feature_names)
        objects=''
        for j in range(len(subgraphs[i])):
            tempList = list(subgraphs[i].nodes())
            filter = df_representation["@@object"].isin([tempList[j]])
            filter = df_representation[filter]
            tempFilter = pd.concat([tempFilter, filter], ignore_index = True)
            objects = objects+" "+tempList[j]


        df_representation_final.loc[i] = [objects]


    df_representation_final.to_csv('temp/graphs.csv',sep=',',index=False)







