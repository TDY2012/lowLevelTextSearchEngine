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
DocIdIndexFileName = 'docId_index.pickle'
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
    parser.add_option( '--textDir',
                        action='store',
                        dest='textDir',
                        default=TextFileDir,
                        help='text file directory (default = {!r})'.format(TextFileDir) )

    (options, args) = parser.parse_args()

    if len(args) != NumRequiredArgs:
        parser.error('Incorrect number of arguments')
        sys.exit(-1)

    #   Parse options
    textDir = options.textDir

    #   Construct text processor
    textProcessor = TextProcessor( textDir,
                                    tokenizerOption=TokenizerOption.REMOVE_STOP_WORDS,
                                    normalizerOption=NormalizerOption.REMOVE_PUNCTUATION | NormalizerOption.CASE_FOLDING )

    #   Write docId index
    textProcessor.writeDocIdIndex( IndexDir, DocIdIndexFileName )

    #   Construct intermediate index
    textProcessor.writeIntermediateIndex( IntermediateIndexDir )

    #   Get docId list
    docIdList = [ x[0] for x in textProcessor.docIdToTextFileNameTupleList ]

    #   Get number of documents
    numDoc = len( docIdList )

    #   Construct indexer
    indexer = Indexer()

    #   Read intermediate index
    indexer.readFromIntermediateIndexDir( IntermediateIndexDir )

    #   Convert index to tf-idf weighted
    indexer.convertIndexToTfIdf( numDoc )

    #   Write to file
    indexer.writeIndex( IndexDir, IndexFileName )

    #   Construct inverted index
    indexer.constructInvertedIndexTfIdf( docIdList )

    #   Normalize inverted index
    indexer.normalizeInvertedIndexTfIdf()

    #   Write to file
    indexer.writeInvertedIndex( IndexDir, InvertedIndexFileName )

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()