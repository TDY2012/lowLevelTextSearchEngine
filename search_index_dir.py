#!/usr/bin/env python

##########################################################################
#   IMPORT
##########################################################################

import sys
from optparse import OptionParser
from indexer.Indexer import Indexer
from querymanager.QueryManager import QueryManager
from textprocessor.Tokenizer import TokenizerOption
from textprocessor.Normalizer import NormalizerOption
from textprocessor.TextProcessor import TextProcessor

##########################################################################
#   GLOBAL
##########################################################################

#TextFileDir = '../dataset/Gutenberg/txt'
TextFileDir = '../dataset/Gutenberg/sample'

NumRequiredArgs = 1
IndexDir = 'index'
IndexFileName = 'index.pickle'
DocIdIndexFileName = 'docId_index.pickle'
InvertedIndexFileName = 'inverted_index.pickle'

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

    parser = OptionParser(usage='usage: %prog [options] <QUERY_STRING>',
                            version='%prog 0.0')

    (options, args) = parser.parse_args()

    if len(args) != NumRequiredArgs:
        parser.error('Incorrect number of arguments')
        sys.exit(-1)

    queryStr = args[0]

    textProcess = TextProcessor( TextFileDir )
    textProcess.readTextFileFromTextFileDir()

    indexer = Indexer()

    indexer.readFromDocIdIndexDir( IndexDir, DocIdIndexFileName )
    indexer.readFromInvertedIndexDir( IndexDir, InvertedIndexFileName )

    queryManager = QueryManager( indexer,
                                TokenizerOption.REMOVE_STOP_WORDS,
                                NormalizerOption.REMOVE_PUNCTUATION | NormalizerOption.CASE_FOLDING )

    resultDict = queryManager.query( queryStr )

    resultDict = { indexer.getDocNameById(x[0]) : x[1] for x in resultDict }

    print(resultDict)

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()