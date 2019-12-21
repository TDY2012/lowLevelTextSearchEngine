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

##########################################################################
#   CLASS
##########################################################################

class QueryManager(object):

    def __init__(self, indexer):
        self.indexer = indexer

    def query( queryStr : str,
                tokenizerOption : Optional[int] = TokenizerOption.NONE,
                normalizerOption : Optional[int] = NormalizerOption.NONE ):

        assert(self.indexer != None)

        queryTermList = Tokenizer.tokenize( queryStr, isRemoveStopWord=tokenizerOption & TokenizerOption.REMOVE_STOP_WORDS )

        queryTermList = Normalizer.normalizeTokenList( queryTermList, isRemovePunctuation=normalizerOption & NormalizerOption.REMOVE_PUNCTUATION,
                                                                        isCaseFolding=normalizerOption & NormalizerOption.CASE_FOLDING )

