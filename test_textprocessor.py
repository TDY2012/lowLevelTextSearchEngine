#!/usr/bin/env python

##########################################################################
#   IMPORT
##########################################################################

import sys
from optparse import OptionParser

from textprocessor.Tokenizer import Tokenizer
from textprocessor.Normalizer import Normalizer

##########################################################################
#   GLOBAL
##########################################################################

NumRequiredArgs = 0

##########################################################################
#   HELPER
##########################################################################

##########################################################################
#   CLASS
##########################################################################

##########################################################################
#   MAIN
##########################################################################

def main():

    parser = OptionParser(usage='usage: %prog [options]',
                            version='%prog 0.0')

    (options, args) = parser.parse_args()

    if len(args) != NumRequiredArgs:
        parser.error('Incorrect number of arguments')
        sys.exit(-1)

    #   Define a sample text
    text = 'This is a red book.'

    #   Do tokenize
    tokenList = Tokenizer.tokenize( text )

    #   Do normalize
    tokenList = Normalizer.normalizeTokenList( tokenList )

    print(tokenList)

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()