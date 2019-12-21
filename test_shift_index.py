import os
import ast
import re

intermediateIndexDir = 'intermediate_index'
intermediateIndexFileNameFormat = 'intermediate_index_{id}.txt'
shiftedIntermediateIndexFileNameFormat = 'shifted_intermediate_index_{id}.txt'

def shiftIntermediateIndex( intermediateIndex, shiftIndex, multiplier=379 ):

    shiftedIntermediateIndex = dict()
    for term, docIdToTermFreqDict in intermediateIndex.items():
        shiftedIntermediateIndex[term] = { docId+(shiftIndex*multiplier) : termFreq for docId, termFreq in docIdToTermFreqDict.items() }

    return shiftedIntermediateIndex

#   Check if intermediate index directory exists
if not os.path.exists( intermediateIndexDir ):
    raise ValueError('readIntermediateIndex() - Cannot find intermediate index directory at {}.'.format(intermediateIndexDir))

#   List all file inside intermediate index directory
fileNameList = os.listdir( intermediateIndexDir )

#   Get only intermediate index file name from list
intermediateIndexFileNameList = [ fileName for fileName in fileNameList if re.match( intermediateIndexFileNameFormat.format( **{'id':'([0-9]+)'} ), fileName ) ]

#   Initialzie intermediate index data list
intermediateIndexDataList = list()

for intermediateIndexFileName in intermediateIndexFileNameList:
    
    #   Read intermediate file
    with open(os.path.join(intermediateIndexDir, intermediateIndexFileName), 'r', encoding='utf-8') as intermediateIndexFile:
        serializedIntermediateIndexStr = intermediateIndexFile.read()

    #   Get intermediate index id from name
    matched = re.match( intermediateIndexFileNameFormat.format( **{'id':'([0-9]+)'} ), intermediateIndexFileName )
    intermediateIndexId = int(matched.group(1))

    #   Parse read serialized string as dictionary
    intermediateIndex = ast.literal_eval( serializedIntermediateIndexStr )

    intermediateIndex = shiftIntermediateIndex( intermediateIndex, intermediateIndexId )

    #   Write shifted intermediate file
    with open(os.path.join(intermediateIndexDir, shiftedIntermediateIndexFileNameFormat.format( **{'id':intermediateIndexId})), 'w', encoding='utf-8') as intermediateIndexFile:
        intermediateIndexFile.write(repr(intermediateIndex))