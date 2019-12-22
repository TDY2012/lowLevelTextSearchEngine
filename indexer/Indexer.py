##########################################################################
#   IMPORT
##########################################################################

import os
import re
import ast
import math
import pickle
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

def normalizeInvertedIndex( invertedIndex : Dict ) -> Dict:
    ''' This function normalizes each document vector in tf-idf weighted
        inverted index
    '''

    for docId, termToWeightedTfIdfDict in invertedIndex.items():

        #   Compute document vector size
        docVectorSize = math.sqrt(sum([ weightedTfIdf**2 for weightedTfIdf in termToWeightedTfIdfDict.values()]))

        #   Normalize each weighted td-idf with document vector size
        invertedIndex[docId] = { term: weightedTfIdf/docVectorSize for term, weightedTfIdf in termToWeightedTfIdfDict.items() }

    return invertedIndex

##########################################################################
#   CLASS
##########################################################################

class Indexer(object):

    def __init__(self):
        self.index = None
        self.invertedIndex = None
        self.docIdIndex = None

    def readFromDocIdIndexDir( self, docIdIndexDir : str, docIdIndexFileName : str, isUsePickle : Optional[bool] = True ):
        ''' This function reads docId index from index directory
        '''

        #   Construct docId index file path
        docIdIndexFilePath = os.path.join( docIdIndexDir, docIdIndexFileName )

        #   Check if index file path exists
        if not os.path.exists( docIdIndexFilePath ):
            raise ValueError('readFromDocIdIndexDir() - Cannot find docId index file at {}.'.format(docIdIndexFilePath))

        if isUsePickle:

            #   Read index file
            with open( docIdIndexFilePath, 'rb' ) as docIdIndexFile:
                self.docIdIndex = dict(pickle.load( docIdIndexFile ))

        else:

            #   Read index file
            with open( docIdIndexFilePath, 'r', encoding='utf-8' ) as docIdIndexFile:
                serializedDocIdIndexStr = docIdIndexFile.read()
                self.docIdIndex = dict(ast.literal_eval( serializedDocIdIndexStr ))

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

    def readFromIndexDir( self, indexDir : str, indexFileName : str, isUsePickle : Optional[bool] = True ):
        ''' This function reads index from index directory
        '''

        #   Construct index file path
        indexFilePath = os.path.join( indexDir, indexFileName )

        #   Check if index file path exists
        if not os.path.exists( indexFilePath ):
            raise ValueError('readFromIndexDir() - Cannot find index file at {}.'.format(indexFilePath))

        if isUsePickle:

            #   Read index file
            with open( indexFilePath, 'rb' ) as indexFile:
                self.index = pickle.load( indexFile )

        else:

            #   Read index file
            with open( indexFilePath, 'r', encoding='utf-8' ) as indexFile:
                serializedIndexStr = indexFile.read()
                self.index = ast.literal_eval( serializedIndexStr )

    def readFromInvertedIndexDir( self, invertedIndexDir : str, invertedIndexFileName : str, isUsePickle : Optional[bool] = True ):
        ''' This function reads inverted index from index directory
        '''

        #   Construct inverted index file path
        invertedIndexFilePath = os.path.join( invertedIndexDir, invertedIndexFileName )

        #   Check if inverted index file path exists
        if not os.path.exists( invertedIndexFilePath ):
            raise ValueError('readFromIndexDir() - Cannot find inverted index file at {}.'.format(invertedIndexFilePath))

        if isUsePickle:

            #   Read inverted index file
            with open( invertedIndexFilePath, 'rb' ) as invertedIndexFile:
                self.invertedIndex = pickle.load( invertedIndexFile )

        else:

            #   Read inverted index file
            with open( invertedIndexFilePath, 'r', encoding='utf-8' ) as invertedIndexFile:
                serializedInvertedIndexStr = invertedIndexFile.read()
                self.invertedIndex = ast.literal_eval( serializedInvertedIndexStr )

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

    def constructInvertedIndexTfIdf( self, docIdList : List[int] ):
        ''' This function constructs inverted index of the index
        '''

        assert( self.index != None )

        #   Initialize inverted index
        self.invertedIndex = { docId : dict() for docId in docIdList }

        #   Invert term and docId indexing structure
        for term, docIdToWeightedTfIdfDict in self.index.items():
            for docId, weightedTfIdf in docIdToWeightedTfIdfDict.items():
                self.invertedIndex[docId][term] = weightedTfIdf

    def normalizeInvertedIndexTfIdf( self ):
        ''' This function normalizes inverted index
        '''

        assert( self.invertedIndex != None )

        self.invertedIndex = normalizeInvertedIndex( self.invertedIndex )

    def writeIndex( self, indexDir : str, indexFileName : str, isUsePickle : Optional[bool] = True ):
        ''' This function writes index file at given path
        '''

        assert( self.index != None )

        #   Construct index file path
        indexFilePath = os.path.join( indexDir, indexFileName )

        if isUsePickle:

            #   Write index file
            with open( indexFilePath, 'wb' ) as indexFile:
                pickle.dump( self.index, indexFile )

        else:

            #   Write index file
            with open( indexFilePath, 'w', encoding='utf-8' ) as indexFile:
                indexFile.write( repr(self.index) )

    def writeInvertedIndex( self, invertedIndexDir : str, invertedIndexFileName : str, isUsePickle : Optional[bool] = True ):
        ''' This function writes inverted index file at given path
        '''

        assert( self.invertedIndex != None )

        #   Construct inverted index file path
        invertedIndexFilePath = os.path.join( invertedIndexDir, invertedIndexFileName )

        if isUsePickle:

            #   Write index file
            with open( invertedIndexFilePath, 'wb' ) as invertedIndexFile:
                pickle.dump( self.invertedIndex, invertedIndexFile )

        else:

            #   Write index file
            with open( invertedIndexFilePath, 'w', encoding='utf-8' ) as invertedIndexFile:
                invertedIndexFile.write( repr(self.invertedIndex) )

    def getDocNameById( self, docId : int ) -> str:
        ''' This function maps docId for document name
        '''

        assert( self.docIdIndex != None )

        return self.docIdIndex[ docId ]