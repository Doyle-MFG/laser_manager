import sys
import os
from PyQt4 import QtCore, QtGui, uic, QtSql

sys.path.insert(0, os.path.split(__file__)[0])

import dbConnection
import report
import functions
from query import query


class Schedule(QtGui.QMainWindow):
    """
    Schedule
    This is the schedule screen. It is used to generate the schedule for each laser
    """
    updateSchedule = QtCore.pyqtSignal(object)
    schedule_qry = None
    schedule_data = None

    def __init__(self, schedule, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setObjectName("Schedule")
        self.resize(931, 637)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/production.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.title = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Terminus")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.horizontalLayout.addWidget(self.title)
        spacerItem = QtGui.QSpacerItem(478, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 919, 530))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.scheduleFrame = QtGui.QFrame(self.scrollAreaWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scheduleFrame.sizePolicy().hasHeightForWidth())
        self.scheduleFrame.setSizePolicy(sizePolicy)
        self.scheduleFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.scheduleFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.scheduleFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scheduleFrame)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(-1, 4, -1, 5)
        self.horizontalLayout_2.addWidget(self.scheduleFrame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout.setStretch(2, 1)
        self.setCentralWidget(self.centralwidget)
        self.schedule = schedule
        self.setWindowTitle("%s Manager" % self.schedule)
        self.title.setText("%s Manager" % self.schedule)
        #Connect to the update signal
        self.updateSchedule.connect(self.update_schedule_)
        
        #Load all the schedule data from the database
        self.get_schedule_data()
        
    def get_schedule_data(self, qry=None):
        """
        This function retrieved all the required data from the database
        and sends it to the display function. It also sets up a time to check
        for new updates once a second.
        """
        #If qry was passed, use the data from it instead of rerunning the query
        if qry is None:
            self.schedule_qry = query("work_schedule", [self.schedule])
            if not self.schedule_qry:
                return False
        else:
            self.schedule_qry = qry
            self.schedule_qry.seek(-1)
        
        #self.scheduleData is used to check if the schedule needs updated
        self.schedule_data = []
        
        while self.schedule_qry.next():
            row = []
            for i in range(10):
                row.append(self.schedule_qry.value(i))
            self.schedule_data.append(row)
            
            pdfqry = query("work_order_pdf_check", [self.schedule_qry.value(8).toString()])
            if pdfqry:
                if pdfqry.first():
                    hasprint = True
                else:
                    hasprint = False
            else:
                hasprint = False
            
            #Send the data to the display function so it can be added
            #to the layout.
            self.new_row(self.schedule_qry.record(), hasprint)
            
        #Pushes all the rows together at the top of the page
        self.scheduleFrame.layout().insertStretch(-1)
        
        #Set up update timer. Currently set to update once a second.
        self.startTimer(1000)
        return True
    
    def timerEvent(self, event):
        """
        This function reruns the schedule query and then checks for
        changes in the data. If changes are found, the data is updated.
        """
        qry = query("work_schedule", [self.schedule])
        if qry:
            new_data = []
            #Build a list so it can be compared for differences.
            while qry.next():
                row = []
                for i in range(10):
                    row.append(qry.value(i))
                new_data.append(row)
            if new_data != self.schedule_data:
                #If new data is found, emit the update signal and pass
                #the query so it doesn't have to be reran.
                self.updateSchedule.emit(qry)
                QtGui.QApplication.alert(self)
        else:
            self.killTimer(event.timerId())
            event.ignore()
    
    def update_schedule_(self, qry):
        """
        Called when the schedule needs updated.
        Removes all the current row widgets then calls the schedule data
        function and passes the check query to prevent it from being reran.
        """
        layout = self.scheduleFrame.layout()
        functions.clear_layout(layout)
        self.get_schedule_data(qry)
        return
    
    def new_row(self, rec, has_print):
        """
        Lays out the Gui for a new row using the data from rec
        """
        row = functions.NewRow()
        row.priority.setText(rec.value(0).toString().rightJustified(3, QtCore.QChar('0')))
        row.job_number.setText(rec.value(1).toString())
        row.notes.setPlainText(rec.value(9).toString())
        row.material.setText(rec.value(3).toString())
        row.material_qty.setText(rec.value(4).toString())
        row.running = rec.value(5).toString()
        row.finished = rec.value(6).toString()
        row.modifying = rec.value(7).toString()
        row.job = rec.value(8).toString()
        
        row.material.setCompleter(functions.MaterialCompleter())
        
        row.print_report.setEnabled(has_print)
        
        #Sets the different row styles depending on the row status
        row = functions.set_row_style(row)

        row.modified = False
        
        row.print_report.clicked.connect(self.print_report)
        row.hide_job.clicked.connect(self.hide_job_)
        row.edit_job.clicked.connect(self.edit_job_)
        row.upload_pdf.clicked.connect(self.upload_report_)
        
        row.priority.textEdited.connect(self.row_edited)
        row.material.textEdited.connect(self.row_edited)
        row.material_qty.textEdited.connect(self.row_edited)
        
        row.priority.editingFinished.connect(self.row_editing_finished)
        row.material.editingFinished.connect(self.row_editing_finished)
        row.material_qty.editingFinished.connect(self.row_editing_finished)
        
        self.scheduleFrame.layout().addWidget(row)
        return
        
    def hide_job_(self):
        """
        Called via signal. Hides the sender row.
        """
        #Find the sender
        job_num = self.sender().parent().job
        
        #Open the connection to the master database server
        dbw, ok = dbConnection.new_connection('write', 'riverview', 'riverview')
        if not ok:
            dbConnection.db_err(dbw)
            return False
        qry = query("finish_work_order", [job_num], dbw)

        #Update the show status to False
        if qry:
            QtGui.QMessageBox.information(self, 'Successful', 'Job %s has been hidden' % job_num)
            return True
        else:
            return False

    def edit_job_(self):
        """
        Called via signal. Marks the sender row as being modified.
        """
        #Find the sender
        job_num = self.sender().parent().job
        
        #Open the connection to the master database server
        dbw, ok = dbConnection.new_connection('write', 'riverview', 'riverview')
        if not ok:
            dbConnection.db_err(dbw)
            return False
        qry = query("modify_work_order", [job_num], dbw)
        if qry:
            QtGui.QMessageBox.information(self, 'Successful', 'The edit status for Job %s as been changed' % job_num)
            return True
        else:
            return False

    def row_edited(self):
        """
        Marks the current row as red if it has been modified
        """
        #Find the sender
        row = self.sender().parent()
        row.setStyleSheet('background-color:rgb(200,40,40);')
    
    def row_editing_finished(self):
        """
        Saves the current row data to the database
        """
        #Find the sender
        row = self.sender().parent()
        data = [row.job, row.priority.text(), 
                row.material.text(), row.material_qty.text()]
        dbw, ok = dbConnection.new_connection('write', 'riverview', 'riverview')
        if ok:
            qry = query("update_work_order", data, dbw)
            if qry:
                row.setStyleSheet('')
    
    def upload_report_(self):
        """
        Function for uploading a pdf to the database so the user can
        print it from their scheduler.
        """
        #Find the sender
        job_num = self.sender().parent().job
        
        #Get the last directory that was used
        last_laser = str(functions.read_settings('last_laser').toString())
        
        #Get the report_file the user wants to upload
        report_file = QtGui.QFileDialog.getOpenFileName(self, caption='Open Print', filter='*.pdf',
                                                        directory=last_laser)
        if report_file:
            functions.write_settings('last_laser', last_laser.rsplit('/', 1)[0])
            print_bin = open(report_file, 'rb')
            dbw, ok = dbConnection.new_connection('write', 'riverview', 'riverview')
            if ok:
                qry = query("insert_pdf", [job_num, print_bin.read().encode('hex')], dbw)
                if qry:
                    QtGui.QMessageBox.information(None, "Successful", "Paperwork Successfully uploaded")
                    self.update_schedule_(None)
                    return True
                else:
                    return False

    def print_report(self):
        """
        Creates/downloads and opens pdf files of the paperwork needed to
        run the sender job.
        
        The part routers are created and the laser sheets are downloaded
        """
        job_num = self.sender().parent().job
        qry = query("get_pdf", [job_num])
        if qry:
            if qry.first():
                pdf_file = '.tmp.pdf'
                with open(pdf_file, 'wb') as f:
                    pdf = qry.value(0).toByteArray()
                    #Write the laser sheet to tmp.pdf
                    f.write(pdf)
                    f.close()
            
                #Determine the correct platform and open the laser sheet
                if sys.platform.startswith('darwin'):
                    os.system('open %s' % pdf_file)
                elif sys.platform.startswith('linux'):
                    os.system('xdg-open %s' % pdf_file)
                elif sys.platform.startswith('win32'):
                    os.startfile('%s' % pdf_file)
            else:
                text = ("No pdf file for the current job could be found in the database. "
                        "If you require one please contact the scheduler."
                        )
                QtGui.QMessageBox.information(self, "No File", text)
        else:
            return False
        
        qry = query("report_header_data", [job_num])
        if qry:
            qry.first()
            h_data = [qry.value(0).toString(), qry.value(1).toString(), qry.value(2).toString(), ]
        else:
            return False

        #Get the individual part information
        qry = query("report_data", [job_num])
        if qry:
            rows = qry.size()
            row_data = []
            while qry.next():
                row_data.append(qry.record())
        else:
            return False
        
        #Get local print location
        prints = functions.read_settings('prints').toString()
        #If the location isn't in the settings file, ask for it then save it.
        if not prints:
            prints = QtGui.QFileDialog.getExistingDirectory(self, 'Prints')
            if prints:
                functions.write_settings('prints', prints)
            else:
                text = "Prints location couldn't be determined."
                QtGui.QMessageBox.critical(self, "Error", text)
                return False
                
        #Generate and save the report to pdf
        report.ind_wo(h_data, rows, row_data, prints)
        
        #Locate and open the report
        pdf_file = "indWo.pdf"
        if sys.platform.startswith('darwin'):
            os.system('open %s' % pdf_file)
        elif sys.platform.startswith('linux'):
            os.system('xdg-open %s' % pdf_file)
        elif sys.platform.startswith('win32'):
            os.startfile('%s' % pdf_file)
        return True