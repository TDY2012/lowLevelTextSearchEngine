##########################################################################
#   IMPORT
##########################################################################

import os
import re
import ast
import math
from typing import Optional, List, Dict
from textprocessor.TextProcessor import IntermediateIndexFileNameFormat

##########################################################################
#   GLOBAL
##########################################################################

IndexFileNameFormat = 'index.txt'

##########################################################################
#   HELPER
##########################################################################

def mergeIntermediateIndex( intermediateIndexList : List ) -> Dict:
    ''' This function merges intermediate indices into one intermediate index
    '''

    assert(len(intermediateIndexList)>0)

    #   Get first intermediate index from list
    mergedIntermediateIndex = intermediateIndexList[0]

    #   Merge the left intermediate indices in list
    for intermediateIndex in intermediateIndexList[1:]:

        for term, docIdToTermFreqDict in intermediateIndex.items():
            if term not in mergedIntermediateIndex:
                mergedIntermediateIndex[term] = docIdToTermFreqDict
            else:
                mergedIntermediateIndex[term].update(docIdToTermFreqDict)

    return mergedIntermediateIndex

##########################################################################
#   CLASS
##########################################################################

class Indexer(object):

    def __init__(self):
        self.index = None

    def readFromIntermediateIndexDir( self, intermediateIndexDir : str, intermediateIndexFileNameFormat : Optional[str] = IntermediateIndexFileNameFormat ):
        ''' This function reads intermediate index from given directory and file name format then
            merges them (if there're more than one) together
        '''

        #   Check if intermediate index directory exists
        if not os.path.exists( intermediateIndexDir ):
            raise ValueError('readIntermediateIndex() - Cannot find intermediate index directory at {}.'.format(intermediateIndexDir))

        #   List all file inside intermediate index directory
        fileNameList = os.listdir( intermediateIndexDir )

        #   Get only intermediate index file name from list
        intermediateIndexFileNameList = [ fileName for fileName in fileNameList if re.match( intermediateIndexFileNameFormat.format( **{'id':'([0-9]+)'} ), fileName ) ]

        #   Initialzie intermediate index data list
        intermediateIndexList = list()

        for intermediateIndexFileName in intermediateIndexFileNameList:
            
            #   Read intermediate index file
            with open(os.path.join(intermediateIndexDir, intermediateIndexFileName), 'r', encoding='utf-8') as intermediateIndexFile:
                serializedIntermediateIndexStr = intermediateIndexFile.read()

            #   Parse read serialized string as dictionary
            intermediateIndex = ast.literal_eval( serializedIntermediateIndexStr )

            #   Add intermediate index to list
            intermediateIndexList.append( intermediateIndex )

        #   Merge intermediate indices
        self.index = mergeIntermediateIndex( intermediateIndexList )

    def readFromIndexDir( self, indexDir : str, indexFileName : str ):
        ''' This function reads index from index directory
        '''

        #   Construct index file path
        indexFilePath = os.path.join( indexDir, indexFileName )

        #   Check if index file path exists
        if not os.path.exists( indexFilePath ):
            raise ValueError('readFromIndexDir() - Cannot find index file at {}.'.format(indexFilePath))

        #   Read index file
        with open( indexFilePath, 'r', encoding='utf-8' ) as indexFile:
            serializedIndexStr = indexFile.read()

        #   Parse read serialized string as dictionary
        self.index = ast.literal_eval( serializedIndexStr )

    def convertIndexToTfIdf( self, numDoc : int ):
        ''' This function converts index in form of just term frequency to
            weighted tf-idf
        '''

        assert( self.index != None )

        for term, docIdToTermFreqDict in self.index.items():
            
            #   Compute document frequency
            docFreq = numDoc/len(docIdToTermFreqDict)

            #   Compute td-idf weight for each term and document
            for docId, termFreq in docIdToTermFreqDict.items():
                self.index[term][docId] = math.log10( 1 + termFreq )*math.log10( docFreq )

    def writeIndex( self, indexDir : str, indexFileName : str ):
        ''' This function writes index file at given path
        '''

        assert( self.index != None )

        #   Construct index file path
        indexFilePath = os.path.join( indexDir, indexFileName )

        #   Write index file
        with open( indexFilePath, 'w', encoding='utf-8' ) as indexFile:
            indexFile.write( repr(self.index) )