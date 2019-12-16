##########################################################################
#   IMPORT
##########################################################################

import os
import re
from typing import Optional

from .Tokenizer import Tokenizer, TokenizerOption
from .Normalizer import Normalizer, NormalizerOption

##########################################################################
#   GLOBAL
##########################################################################

TextFileNamePattern = '(.+)\.txt'

##########################################################################
#   HELPER
##########################################################################

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

        #   Store the validated text file name list
        self.textFileNameList = validTextFileNameList

        #   For test
        self.textFileNameList = self.textFileNameList[0:10]

    def constructIntermediateIndex( self ):
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

        assert( self.textFileNameList != None )

        #   Initialize term to document id to term frequency mapping dictionary
        #   NOTE - document id is indexed by validated text file name list
        termToDocIdToTermFrequencyDict = dict()

        #   For each docId, textFileName enumerate( textFileNameList )
        for docId, textFileName in enumerate( self.textFileNameList ):

            #   Open text file from text file directory
            with open( os.path.join( self.textFileDir, textFileName ) ) as textFile:
                
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

                #   Assign document id and term frequency
                termToDocIdToTermFrequencyDict[token][docId] = tokenList.count(token)

        return termToDocIdToTermFrequencyDict