#!/usr/bin/env python

##########################################################################
#   IMPORT
##########################################################################

import sys
from optparse import OptionParser

from textprocessor.TextProcessor import TextProcessor
from textprocessor.Tokenizer import TokenizerOption
from textprocessor.Normalizer import NormalizerOption

from indexer.Indexer import Indexer

##########################################################################
#   GLOBAL
##########################################################################

NumRequiredArgs = 0

TextFileDir = '../dataset/Gutenberg/txt'

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

    #   Construct text processor
    textProcessor = TextProcessor( TextFileDir,
                                    tokenizerOption=TokenizerOption.REMOVE_STOP_WORDS,
                                    normalizerOption=NormalizerOption.REMOVE_PUNCTUATION | NormalizerOption.CASE_FOLDING )

    #   Construct intermediate index
    #textProcessor.writeIntermediateIndex('intermediate_index')

    numDoc = len( textProcessor.textFileNameList )

    indexer = Indexer()

    # indexer.readFromIntermediateIndexDir( 'intermediate_index' )

    # indexer.convertIndexToTfIdf( numDoc )

    # indexer.writeIndex( 'index', 'index.txt' )

    indexer.readFromIndexDir( 'index', 'index.txt' )

    indexer.constructInvertedIndexTfIdf( numDoc )

    indexer.writeInvertedIndex( 'index', 'inverted_index.txt' )

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()