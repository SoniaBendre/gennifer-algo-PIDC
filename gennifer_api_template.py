import os
import pandas as pd
from pathlib import Path
import uuid
import json
import numpy as np

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data/GSD')


def generateInputs(dataset_uri):
    '''
    Function to generate desired inputs for SCODE.
    If the folder/files under RunnerObj.datadir exist, 
    this function will not do anything.
    '''

    pathToExpressionData = os.path.join(DATASET_PATH, dataset_uri, "ExpressionData.csv")

    if not os.path.join(DATASET_PATH, dataset_uri).exists():   
        print("Input folder for PIDC does not exist, creating input folder...")
        os.path.join(DATASET_PATH, dataset_uri).mkdir(exist_ok = False)
        
        
    if not pathToExpressionData.exists():
        print(f"ExpressionData.cs does not exist at path")
        return
    
    #TODO: converting from csv to tsv -- do i really need to do this?
    ExpressionData = pd.read_csv(pathToExpressionData, header=0, index_col=0)
    ExpressionData.to_csv(pathToExpressionData, sep = '\t', header  = True, index = True)
    return 
    
def run(dataset_uri):
    '''
    Function to run PIDC algorithm
    '''
    uniqueID = str(uuid.uuid4())
    pathToExpressionData = os.path.join(DATASET_PATH, dataset_uri, "ExpressionData.csv")

    
    # make output dirs if they do not exist:
    outDir =  os.path.join("/tmp", uniqueID)
    os.makedirs(outDir, exist_ok = True)
    
    outPath = str(outDir) + 'outFile.txt'

    cmdToRun = ' '.join(['julia runPIDC.jl', pathToExpressionData, outPath ])
    print(cmdToRun)
    os.system(cmdToRun)

    return outDir



def parseOutput(outDir):
    '''
    Function to parse outputs from SCODE.
    '''
    # Quit if output directory does not exist
    if not Path(outDir+'outFile.txt').exists():
        print(outDir+'outFile.txt'+'does not exist, skipping...')
        return
        
    # Read output
    OutDF = pd.read_csv(outDir+'outFile.txt', sep = '\t', header = None)

    results = {'Gene1': [], 
               'Gene2': [],
               'EdgeWeight': []}
    
    outFile = open(outDir + 'rankedEdges.csv','w')
    outFile.write('Gene1'+'\t'+'Gene2'+'\t'+'EdgeWeight'+'\n')

    for idx, row in OutDF.iterrows():
        results['Gene1'].append(row[0])
        results['Gene2'].append(row[1])
        results['Gene1'].append(str(row[2]))
    
    return json.dumps(results)
    
