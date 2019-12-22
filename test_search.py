#!/usr/bin/env python

##########################################################################
#   IMPORT
##########################################################################

import sys
from optparse import OptionParser
from indexer.Indexer import Indexer
from querymanager.QueryManager import QueryManager

##########################################################################
#   GLOBAL
##########################################################################

NumRequiredArgs = 1
IndexDir = 'index'
IndexFileName = 'index.pickle'
InvertedIndexDir = 'index'
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

    indexer = Indexer()

    indexer.readFromInvertedIndexDir( InvertedIndexDir, InvertedIndexFileName )

    print(indexer.invertedIndex)

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()