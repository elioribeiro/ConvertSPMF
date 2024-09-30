from createGraphs import createGraphs
from convertSPMF import convertSPMF


#Download the OCEL file and save it in the OCEL folder.
path = "OCEL/DS1-ExperimentoDois.jsonocel"

createGraphs(path)

outputFileName = "SPMFToolInput"

#The output files are saved in the temp folder
convertSPMF(path,outputFileName)