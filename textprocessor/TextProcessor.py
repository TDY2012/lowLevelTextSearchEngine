# -*- coding: utf-8 -*-
##########################################################################
#   IMPORT
##########################################################################

import os
import re
import pickle
from typing import Optional
import multiprocessing
import time

from .Tokenizer import Tokenizer, TokenizerOption
from .Normalizer import Normalizer, NormalizerOption

##########################################################################
#   GLOBAL
##########################################################################

TextFileNamePattern = '(.+)\.txt'

IntermediateIndexFileNameFormat = 'intermediate_index_{id}.txt'

NumProcess = 8

##########################################################################
#   HELPER
##########################################################################

def chunkify( l, n ):
    return [ [ l[i] for i in range(j*(len(l)//n),(j+1)*(len(l)//n)) ] for j in range(n-1) ] + [ l[ (n-1)*(len(l)//n): ] ]

##########################################################################
#   CLASS
##########################################################################

class TextProcessor(object):

    def __init__( self, textFileDir : str,
                        textFileNamePattern : Optional[str] = TextFileNamePattern,
                        tokenizerOption : Optional[int] = TokenizerOption.NONE,
                        normalizerOption : Optional[int] = NormalizerOption.NONE ):

        if not os.path.exists( textFileDir ):
            raise ValueError( 'TextProcessor - Input text file directory does not exist at {}.'.format( textFileDir ) )
        elif not os.path.isdir( textFileDir ):
            raise ValueError( 'TextProcessor - {} is not a directory.'.format( textFileDir ) )
        
        self.textFileDir = textFileDir
        self.textFileNamePattern = textFileNamePattern
        self.tokenizerOption = tokenizerOption
        self.normalizerOption = normalizerOption

        #   Read text file
        self.readTextFileFromTextFileDir()

    def readTextFileFromTextFileDir( self ):
        ''' This function reads all text file from given text file directory.
        '''

        assert( self.textFileDir != None )
        assert( self.textFileNamePattern != None )

        #   List all text file from text file directory
        allTextFileNameList = os.listdir( self.textFileDir )

        #   Validate text file name with text file name pattern
        validTextFileNameList = [ fileName for fileName in allTextFileNameList if re.match( self.textFileNamePattern, fileName ) ]

        #   Construct docId to text file name tuple list
        self.docIdToTextFileNameTupleList = list(enumerate(validTextFileNameList))

    def writeDocIdIndex( self, docIdIndexDir : str, docIdIndexFileName : str, isUsePickle : Optional[bool] = True ):
        ''' This function writes docId to text file name mapping dictionary
        '''

        assert( self.docIdToTextFileNameTupleList != None )

        #   Construct docId index file path
        docIdIndexFilePath = os.path.join( docIdIndexDir, docIdIndexFileName )

        if isUsePickle:

            #   Write index file
            with open( docIdIndexFilePath, 'wb' ) as docIdIndexFile:
                pickle.dump( self.docIdToTextFileNameTupleList, docIdIndexFile )

        else:

            #   Write index file
            with open( docIdIndexFilePath, 'w', encoding='utf-8' ) as docIdIndexFile:
                docIdIndexFile.write( repr(self.docIdToTextFileNameTupleList) )

    def writeIntermediateIndex( self, intermediateIndexDir : str,
                                        intermediateIndexFileNameFormat : Optional[str] = IntermediateIndexFileNameFormat,
                                        numProcess : Optional[int] = NumProcess ):
        ''' This function writes intermediate indices to index file directory
            with specified name format by splitting current text file name list into
            chunks and multiprocessing them
        '''

        #   Check if intermediate index file directory exists
        if not os.path.exists(intermediateIndexDir):
            raise ValueError('writeIntermediateIndex() - No directory at {}.'.format(intermediateIndexDir))
        
        #   Inititalize multiprocessing objects
        manager = multiprocessing.Manager()
        outputQueue = manager.Queue()

        #   Split text file name list into small chunks by number of processes
        docIdToTextFileNameTupleListChunk = chunkify( self.docIdToTextFileNameTupleList, numProcess )

        #   Begin timer
        startTime = time.time()

        #   Construct processes to construct intermediate index
        processList = [ multiprocessing.Process( target=self.constructIntermediateIndex, args=( docIdToTextFileNameTupleList, outputQueue, i ) ) for i, docIdToTextFileNameTupleList in enumerate(docIdToTextFileNameTupleListChunk) ]

        #   Start process
        for process in processList:
            process.start()

        #   Join process
        for process in processList:
            process.join()

        #   Get result from output queue
        resultList = [ outputQueue.get() for process in processList ]

        #   Stop timer
        deltaTime = time.time() - startTime

        #   Log timer message
        print('writeIntermediateIndex() - Index time = {} seconds.'.format(deltaTime))

        #   Write result into intermediate index file at given directory
        for i, result in enumerate(resultList):
            with open( os.path.join( intermediateIndexDir, intermediateIndexFileNameFormat.format(**{'id':i}) ), 'w', encoding='utf-8' ) as indexFile:
                indexFile.write( repr(result) )

    def constructIntermediateIndex( self, docIdToTextFileNameTupleList, outputQueue, processId=0 ):
        ''' This function constructs an intermediated index which represents
            a term to document id to term frequency mapping dictionary.
            The index should be in this following format:
                {
                    term1: {
                                doc1: tf1,1,
                                doc2: tf1,2,
                                ...
                            },
                    term2: {
                                doc1: tf2,1,
                                doc2: tf2,2,
                                ...
                            },
                    ...
                }
        '''

        #   Initialize term to document id to term frequency mapping dictionary
        #   NOTE - document id is indexed by validated text file name list
        termToDocIdToTermFrequencyDict = dict()

        #   Get number of text file name list
        numTextFile = len(docIdToTextFileNameTupleList)

        #   For each docId and textFileName
        for docNum, (docId, textFileName) in enumerate( docIdToTextFileNameTupleList ):

            print('[CPU #{}] Now processing {}. ({}/{})'.format(processId, textFileName, docNum+1, numTextFile))

            #   Open text file from text file directory
            with open( os.path.join( self.textFileDir, textFileName ), encoding='utf-8' ) as textFile:
                
                #   Read text from file
                text = textFile.read()

            #   Do tokenize
            tokenList = Tokenizer.tokenize( text, isRemoveStopWord=self.tokenizerOption & TokenizerOption.REMOVE_STOP_WORDS )
                
            #   Do normalize
            tokenList = Normalizer.normalizeTokenList( tokenList, isRemovePunctuation=self.normalizerOption & NormalizerOption.REMOVE_PUNCTUATION,
                                                                        isCaseFolding=self.normalizerOption & NormalizerOption.CASE_FOLDING )

            for token in tokenList:
                
                #   Initialize document id to term frequency dictionary
                if token not in termToDocIdToTermFrequencyDict:
                    termToDocIdToTermFrequencyDict[token] = dict()

                #   Assign offset document id and term frequency
                termToDocIdToTermFrequencyDict[token][docId] = tokenList.count(token)

            print('[CPU #{}] Done processing {}. ({}/{})'.format(processId, textFileName, docNum+1, numTextFile))

        outputQueue.put( termToDocIdToTermFrequencyDict )