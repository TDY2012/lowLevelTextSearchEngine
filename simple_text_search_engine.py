#!/usr/bin/env python3

##########################################################################
#   IMPORT
##########################################################################

import sys
import os
from optparse import OptionParser
from PyQt5 import QtWidgets

from textprocessor.TextProcessor import TextProcessor
from gui.SimpleTextSearchEngineWindow import SimpleTextSearchEngineWindow

##########################################################################
#   GLOBAL
##########################################################################

NumRequiredArgs = 0
IndexDir = 'index'
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

    parser = OptionParser(usage='usage: %prog [options]',
                            version='%prog 0.0')
    parser.add_option( '--debug',
                        dest='isDebug',
                        action='store_true',
                        default=False,
                        help='enable debug mode' )
    (options, args) = parser.parse_args()

    if len(args) != NumRequiredArgs:
        parser.error('Incorrect number of arguments')
        sys.exit(-1)

    #   Parse options
    isDebug = options.isDebug

    docIdIndexFilePath = os.path.join( IndexDir, DocIdIndexFileName )

    #   Check if docId index directory exists
    if not os.path.exists( docIdIndexFilePath ):
        print('simple_text_search_engine - Cannot find docId index at {}.'.format(docIdIndexFilePath))
        sys.exit(-1)

    invertedIndexFilePath = os.path.join( IndexDir, InvertedIndexFileName )

    #   Check if inverted index directory exists
    if not os.path.exists( invertedIndexFilePath ):
        print('simple_text_search_engine - Cannot find inverted index at {}.'.format(invertedIndexFilePath))
        sys.exit(-1)

    #   Construct pyqt application
    app = QtWidgets.QApplication([])

    #   Construct simple text search engine window
    simpleTextSearchEngineWindow = SimpleTextSearchEngineWindow( isDebug )

    #   Load indices
    simpleTextSearchEngineWindow.loadIndexDir( IndexDir, DocIdIndexFileName, InvertedIndexFileName )

    #   Show window
    simpleTextSearchEngineWindow.show()

    #   Exit application
    sys.exit(app.exec())

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()