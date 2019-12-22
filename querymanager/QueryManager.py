##########################################################################
#   IMPORT
##########################################################################

import math
from typing import Optional, List, Dict
from textprocessor.Tokenizer import Tokenizer, TokenizerOption
from textprocessor.Normalizer import Normalizer, NormalizerOption

##########################################################################
#   GLOBAL
##########################################################################

##########################################################################
#   HELPER
##########################################################################

def constructQueryVector( queryTermList : List ) -> Dict:
    ''' This function constructs unit query vector as term to nomralized
        weight td-idf dictionary
    '''

    return { queryTerm: 1/math.sqrt(len(queryTermList)) for queryTerm in queryTermList }

def computeCosineSimilarity( queryVector : Dict, docVector : Dict ) -> float:
    ''' This function computes cosine similarity between query vector and
        document vector
        NOTE - Assume that both vectors are unit vectors
    '''

    #   Get common term of both vectors
    commonTermSet = set(queryVector.keys()).intersection(set(docVector.keys()))

    #   Compute cosine similarity value
    cosineSimilarity = sum( [ queryVector[term]*docVector[term] for term in commonTermSet ] )

    return cosineSimilarity

##########################################################################
#   CLASS
##########################################################################

class QueryManager(object):

    def __init__(self, indexer,
                        tokenizerOption : Optional[int] = TokenizerOption.NONE,
                        normalizerOption : Optional[int] = NormalizerOption.NONE):
        self.indexer = indexer
        self.tokenizerOption = tokenizerOption
        self.normalizerOption = normalizerOption

    def query( self, queryStr : str ):

        assert(self.indexer != None)

        queryTermList = Tokenizer.tokenize( queryStr, isRemoveStopWord=self.tokenizerOption & TokenizerOption.REMOVE_STOP_WORDS )

        queryTermList = Normalizer.normalizeTokenList( queryTermList, isRemovePunctuation=self.normalizerOption & NormalizerOption.REMOVE_PUNCTUATION,
                                                                        isCaseFolding=self.normalizerOption & NormalizerOption.CASE_FOLDING )

        queryVector = constructQueryVector( queryTermList )

        docIdToConsineSimilarityTupleList = [ (docId, computeCosineSimilarity( queryVector, self.indexer.invertedIndex[docId] )) for docId in self.indexer.invertedIndex.keys() ]

        docIdToConsineSimilarityTupleList.sort( key=lambda x: x[1], reverse=True )

        return docIdToConsineSimilarityTupleList
