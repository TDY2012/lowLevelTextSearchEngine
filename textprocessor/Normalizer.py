##########################################################################
#   IMPORT
##########################################################################

import re

from typing import Optional, List, Set

##########################################################################
#   GLOBAL
##########################################################################

PunctuationCharPattern = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

##########################################################################
#   HELPER
##########################################################################

##########################################################################
#   CLASS
##########################################################################

class EmptyStringException(Exception):
    pass

class NormalizerOption(object):
    NONE = 0
    REMOVE_PUNCTUATION = 1 << 0
    CASE_FOLDING = 1 << 1

class Normalizer(object):

    @staticmethod
    def normalizeTokenList( tokenList : List[str], isRemovePunctuation : Optional[bool] = True, isCaseFolding : Optional[bool] = True ) -> List[str]:
        ''' This function normalizes given token list by optionally removing
            punctuations and applying case folding.
        '''

        #   Initialized normalized token list
        normalizedTokenList = list()

        for token in tokenList:

            #   Try normalize token or skip it if there is a problem
            try:
                normalizedToken = Normalizer.normalize( token, isRemovePunctuation=isRemovePunctuation, isCaseFolding=isCaseFolding )
            except ValueError:
                continue
            
            #   Append normalized token to list
            normalizedTokenList.append( normalizedToken )

        return normalizedTokenList

    @staticmethod
    def normalize( text : str, isRemovePunctuation : Optional[bool] = True, isCaseFolding : Optional[bool] = True ) -> str:
        ''' This function normalizes given text (token) by optionally removing
            punctuations and applying case folding.
        '''

        #   Check if is remove punctuation flag is set
        if isRemovePunctuation:
            try:
                text = Normalizer.removePunctuation(text)
            except EmptyStringException as e:
                raise ValueError( 'normalize() - The normalized text is empty string.' ) from e
        
        #   Check if is case folding flag is set
        if isCaseFolding:
            text = text.casefold()

        return text

    @staticmethod
    def removePunctuation( text : str, punctuationCharPattern : Optional[str] = PunctuationCharPattern ) -> str:
        ''' This function removes all punctuations from given text.
        '''

        #   Remove all punctuation
        text = re.sub('[{}]'.format(punctuationCharPattern), '', text)

        #   Check if the replace text is empty string
        if text == '' or text.isspace():
            raise EmptyStringException( 'removePunctuation() - The text is punctuation.' )

        return text