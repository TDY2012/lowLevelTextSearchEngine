##########################################################################
#   IMPORT
##########################################################################

from typing import Optional, List, Set

##########################################################################
#   GLOBAL
##########################################################################

StopWordSet = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again',
                'there', 'about', 'once', 'during', 'out', 'very', 'having',
                'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its',
                'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off',
                'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
                'themselves', 'until', 'below', 'are', 'we', 'these', 'your','his',
                'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this',
                'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to',
                'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them',
                'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves',
                'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did',
                'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where',
                'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom',
                't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it',
                'how', 'further', 'was', 'here', 'than'}

##########################################################################
#   HELPER
##########################################################################

##########################################################################
#   CLASS
##########################################################################

class TokenizerOption(object):
    NONE = 0
    REMOVE_STOP_WORDS = 1 << 0

class Tokenizer(object):

    @staticmethod
    def tokenize( text : str, isRemoveStopWord : Optional[bool] = True ) -> List[str]:
        ''' This function tokenizes string into list of tokens.
        '''

        #   Simply split input text by space characters (white space, tab, newline)
        tokenList = text.split()

        #   Check if is remove stop word flag is set
        if isRemoveStopWord:
            tokenList = Tokenizer.removeStopWordFromTokenList( tokenList )

        return tokenList

    @staticmethod
    def removeStopWordFromTokenList( tokenList : List[str], stopWordSet : Optional[Set[str]] = StopWordSet ) -> List[str]:
        ''' This function filters out stop words from given token list.
        '''

        return [ token for token in tokenList if token not in stopWordSet ]

        