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

#TextFileDir = '../dataset/Gutenberg/txt'
TextFileDir = '../dataset/Gutenberg/sample'

IndexDir = 'index'
IndexFileName = 'index.pickle'
InvertedIndexFileName = 'inverted_index.pickle'
IntermediateIndexDir = 'intermediate_index'

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
    textProcessor.writeIntermediateIndex( IntermediateIndexDir )

    #   Get number of documents
    numDoc = len( textProcessor.textFileNameList )

    #   Construct indexer
    indexer = Indexer()

    #   Read intermediate index
    indexer.readFromIntermediateIndexDir( IntermediateIndexDir )

    #   Convert index to tf-idf weighted
    indexer.convertIndexToTfIdf( numDoc )

    #   Write to file
    indexer.writeIndex( IndexDir, IndexFileName )

    #   Construct inverted index
    indexer.constructInvertedIndexTfIdf( numDoc )

    #   Write to file
    indexer.writeInvertedIndex( IndexDir, InvertedIndexFileName )

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()