"""
CL850 Manager
    Small app to manage job priority and status for our CL850.

Jobs are color coded and sorted by priority so the user knows at a glance
what job needs ran next and what the coming work load looks like. Color coding 
is listed below for reference. 

From this interface the scheduler can add, remove, and make changes
to the schedule. If the scheduler needs to change a program, it is disabled
and struck out until the changes are finished being made. 

From the other interface users can print both the work order routers and the 
laser job sheets. One can also start jobs, marking them with bold font and
finish job, updating all the part statuses and marking the job dark gray so
it can be removed from the queue.

Priority Color Codes:
    (0)Red - Needs to be ran ASAP
    (1)Orange - Need the parts the next day
    (2)Yellow - Need the parts this week
    (3)Green - Standard priority
    (4)Blue - Lowest priority, only run as filler
"""

import sys
import os
from PyQt4 import QtGui

sys.path.insert(0, os.path.split(__file__)[0])

import graphics
import dbConnection
from main import Main

from reportlab.pdfbase import _fontdata_widths_courier #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_courierbold #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_courieroblique #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_courierboldoblique #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_helvetica #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_helveticabold #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_helveticaoblique #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_helveticaboldoblique #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_timesroman #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_timesbold #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_timesitalic #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_timesbolditalic #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_symbol #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_widths_zapfdingbats #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_enc_winansi #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_enc_macroman #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_enc_standard #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_enc_symbol #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_enc_zapfdingbats #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_enc_pdfdoc #@UnresolvedImport @UnusedImport
from reportlab.pdfbase import _fontdata_enc_macexpert #@UnresolvedImport @UnusedImport


#Colors
def colors():
    return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not dbConnection.default_connection():
        sys.exit(1)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())
