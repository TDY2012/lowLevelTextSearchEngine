##########################################################################
#   IMPORT
##########################################################################

import os
import time

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from .PyQtHelper import getIntValidator
from indexer.Indexer import Indexer
from textprocessor.Tokenizer import TokenizerOption
from textprocessor.Normalizer import NormalizerOption
from textprocessor.TextProcessor import TextProcessor
from querymanager.QueryManager import QueryManager

##########################################################################
#   GLOBAL
##########################################################################

DefaultMaxResultNum = 10

WindowTitle = 'Simple Text Search Engine'

##########################################################################
#   HELPER
##########################################################################

def logResult( queryManger, docIdToCosineSimilaryTupleList ):
    ''' This function logs out formatted results in terminal
    '''

    #   If there is no matching
    if len(docIdToCosineSimilaryTupleList) == 0:
        print('No matched result.')
        return

    print(docIdToCosineSimilaryTupleList)

##########################################################################
#   CLASS
##########################################################################

class QueryThread( QtCore.QThread ):

    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, queryManager, queryStr, isDebug=False):
        QtCore.QThread.__init__(self)
        self.queryManager = queryManager
        self.queryStr = queryStr
        self.isDebug = isDebug

    def run(self):
        
        #   Start timer
        startTime = time.time()

        #   Do query
        docIdToCosineSimilaryTupleList = self.queryManager.query( self.queryStr )

        #   End timer
        deltaTime = time.time() - startTime
        
        if self.isDebug:

            #   Display timer log message
            print( 'Queried in {} seconds.'.format( deltaTime ) )

        #   Return result
        self.signal.emit( docIdToCosineSimilaryTupleList )

class SimpleTextSearchEngineWindow( QtWidgets.QMainWindow ):

    def __init__(self, isDebug=False):
        super(SimpleTextSearchEngineWindow, self).__init__()
        self.isDebug = isDebug
        self.maxResultNum = DefaultMaxResultNum
        self.setWindowTitle( WindowTitle )
        self.createGuiComponents()
        self.initializeGuiComponents()

    def createGuiComponents(self):
        
        widget = QtWidgets.QWidget()

        mainLayout = QtWidgets.QVBoxLayout()

        #   Initialize top, mid and bottom layout
        #   as horizontal box layout
        topLayout = QtWidgets.QHBoxLayout()
        bottomLayout = QtWidgets.QHBoxLayout()

        #
        #   Search Option
        #

        #   Create search option group box widget
        groupBoxSearchOption = QtWidgets.QGroupBox('Search Options')

        #   Create search option form layout
        formLayoutSearchOption = QtWidgets.QFormLayout()

        #   Create max result line edit widget
        self.lineEditMaxResult = QtWidgets.QLineEdit()
        self.lineEditMaxResult.setValidator( getIntValidator(bottomValue=1) )

        #   Create key word line edit widget
        self.lineEditKeyWord = QtWidgets.QLineEdit()

        #   Assign max result line edit widget
        #   and key word line edit widget to
        #   search option group box form layout
        formLayoutSearchOption.addRow( 'Max Result', self.lineEditMaxResult )
        formLayoutSearchOption.addRow( 'Key Word', self.lineEditKeyWord )
        
        #   Set search option group box layout
        groupBoxSearchOption.setLayout(formLayoutSearchOption)

        #
        #   Search Button
        #

        self.buttonSearch = QtWidgets.QPushButton()
        self.buttonSearch.setText( 'Search' )
        self.buttonSearch.setSizePolicy( QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum )

        topLayout.addWidget(groupBoxSearchOption)
        topLayout.addWidget(self.buttonSearch)

        #
        #   Result Table
        #

        #   Create result group box widget
        groupBoxResult = QtWidgets.QGroupBox('Result')

        #   Create result vertical layout
        vBoxResult = QtWidgets.QVBoxLayout()

        #   Create result table widget
        self.tableResult = QtWidgets.QTableWidget()
        self.tableResult.setRowCount(0)
        self.tableResult.setColumnCount(3)
        self.tableResult.setHorizontalHeaderLabels(['Score', 'Id', 'Name'])
        self.tableResult.setSortingEnabled(True)
        self.tableResult.setEditTriggers( QtWidgets.QAbstractItemView.NoEditTriggers )

        vBoxResult.addWidget(self.tableResult)

        #   Set result group box layout
        groupBoxResult.setLayout(vBoxResult)

        bottomLayout.addWidget(groupBoxResult)

        mainLayout.addLayout( topLayout )
        mainLayout.addLayout( bottomLayout )
        
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def initializeGuiComponents( self ):
        ''' This function sets default value and callback function
            to all gui components
        '''

        #   Set default value and callback function
        #   for max result line edit widget
        self.lineEditMaxResult.setText(str(DefaultMaxResultNum))
        self.lineEditMaxResult.textEdited.connect( self.lineEditMaxResult_cb )

        #   Set callback function for search button
        self.buttonSearch.clicked.connect( self.buttonSearch_cb )

    def loadIndexDir( self, indexDir, docIdIndexFileName, invertedIndexFileName ):
        ''' This function loads inverted index and docId index from index directory
            object stored in this class instance for further
            querying
        '''

        self.indexer = Indexer()
        self.indexer.readFromDocIdIndexDir( indexDir, docIdIndexFileName )
        self.indexer.readFromInvertedIndexDir( indexDir, invertedIndexFileName )

        #   Construct query manager
        self.queryManager = QueryManager( self.indexer,
                                        TokenizerOption.REMOVE_STOP_WORDS,
                                        NormalizerOption.REMOVE_PUNCTUATION | NormalizerOption.CASE_FOLDING )

    def lineEditMaxResult_cb( self ):
        ''' This is callback function of max result line edit widget
            which sets maximum result number to query manager
        '''

        #   Check if query manager is initialized
        if not hasattr( self, 'queryManager' ):
            return

        try:
            #   Get max result number from max result line edit widget
            maxResultNum = int(self.lineEditMaxResult.text())
        except ValueError:
            self.lineEditMaxResult.setText(str(DefaultMaxResultNum))
            maxResultNum = DefaultMaxResultNum

        #   NOTE -  This is a hack, since I don't know why int validator
        #           cannot handle 0, despite the buttom value = 1
        if maxResultNum < 1:
            self.lineEditMaxResult.setText(str(1))
            maxResultNum = 1

        #   Set max result number
        self.maxResultNum = maxResultNum

    def buttonSearch_cb( self ):
        ''' This is callback function of search button widget
            which performs querying and displays results on
            results table widget
        '''

        #   Check if query manager is initialized
        if not hasattr( self, 'queryManager' ):
            raise ValueError( 'buttonSearch_cb() - Query manager is not initialized.' )

        #   Get query string from keyword line edit widget
        queryStr =  self.lineEditKeyWord.text()

        #   Begin query with thread
        self.beginQuery( queryStr )

    def beginQuery( self, queryStr ):
        ''' This function constructs query thread and runs it
        '''

        #   Disable the search button while querying
        self.buttonSearch.setEnabled(False)

        #   Construct query thread
        self.queryThread = QueryThread( self.queryManager, queryStr, self.isDebug )

        #   Bind query thread signal to finish query function
        self.queryThread.signal.connect( self.finishQuery )

        #   Run query thread
        self.queryThread.start()

    def finishQuery( self, docIdToCosineSimilaryTupleList ):
        ''' This function gets result from query thread and
            displays result on table widget
        '''

        if self.isDebug:
            
            #   Display log message in terminal
            logResult( self.queryManager, docIdToCosineSimilaryTupleList )

        #   Display result on table widget
        self.displayResultsOnTable( docIdToCosineSimilaryTupleList )

        #   Reenable search button
        self.buttonSearch.setEnabled(True)

    def displayResultsOnTable( self, docIdToCosineSimilaryTupleList ):
        ''' This function populates results table widget with given
            result docId to cosine similiarity tuple list
        '''

        #   If there is no result, clear all result on table
        if len(docIdToCosineSimilaryTupleList) == 0:
            self.tableResult.setRowCount(0)
            return

        #   Limit result with max result number
        docIdToCosineSimilaryTupleList = docIdToCosineSimilaryTupleList[:self.maxResultNum]

        #   Set table row
        self.tableResult.setRowCount(len(docIdToCosineSimilaryTupleList))

        #   Populate record on table
        for resultIndex, docIdToCosineSimilaryTuple in enumerate( docIdToCosineSimilaryTupleList ):
            self.tableResult.setItem( resultIndex, 0, QtWidgets.QTableWidgetItem( str(docIdToCosineSimilaryTuple[1]) ))
            self.tableResult.setItem( resultIndex, 1, QtWidgets.QTableWidgetItem( str(docIdToCosineSimilaryTuple[0]) ))
            self.tableResult.setItem( resultIndex, 2, QtWidgets.QTableWidgetItem( self.indexer.getDocNameById( docIdToCosineSimilaryTuple[0] ) ))