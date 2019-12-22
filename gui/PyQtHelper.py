from typing import Optional
from PyQt5 import QtGui

def getIntValidator( bottomValue : Optional[int] = None, topValue : Optional[int] = None ) -> QtGui.QIntValidator:
    ''' This is a wrapper function for create a QIntValidator
        with easily settable bottom and top value
    '''

    validator = QtGui.QIntValidator()
    
    if bottomValue != None:
        validator.setBottom( bottomValue )
    if topValue != None:
        validator.setTop( topValue )

    return validator