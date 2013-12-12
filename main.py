import sys
import os
from PyQt4 import QtCore, QtGui, uic

sys.path.insert(0, os.path.split(__file__)[0])

import dbConnection
import functions
from schedule import Schedule


class Main(QtGui.QMainWindow):
    """
    Main window
    """
    updateSchedule = QtCore.pyqtSignal(object)
    schedule_qry = None
    schedule_data = None

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.setObjectName("Laser Schedule")
        self.resize(1024, 768)
        
        #Restore the size and position of the window from the settings file
        geometry = functions.read_settings('geometry').toByteArray()
        window_state = functions.read_settings('windowState').toByteArray()
        if geometry:
            self.restoreGeometry(geometry)
        if window_state:
            self.restoreState(window_state)

        self.cl850 = Schedule("cl850", self)
        self.cl940 = Schedule("cl940", self)

        self.tool_box = QtGui.QToolBox()
        self.setCentralWidget(self.tool_box)
        self.tool_box.addItem(self.cl850, "CL850")
        self.tool_box.addItem(self.cl940, "CL940")
        db = dbConnection.DatabaseSettings()

    def closeEvent(self, event):
        """
        Housekeeping when the app closes
        """
        
        #Close all open database connections
        dbConnection.close_all_connections()
        
        #Save size and position information
        functions.write_settings('geometry', self.saveGeometry())
        functions.write_settings('windowState', self.saveState())
        event.accept()