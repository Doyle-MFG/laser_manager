from PyQt4 import QtCore, QtGui, QtSql
from dbConnection import db_err

colors = (QtGui.QColor(215, 40, 40), QtGui.QColor(215, 130, 25), QtGui.QColor(205, 195, 25),
          QtGui.QColor(40, 190, 40), QtGui.QColor(60, 60, 255))


def write_settings(name, value):
    settings = QtCore.QSettings("Doyle Mfg", "CL850 Manager")
    settings.setDefaultFormat(1)
    settings.beginGroup('main')
    settings.setValue(name, value)
    settings.endGroup()


def read_settings(name):
    settings = QtCore.QSettings("Doyle Mfg", "CL850 Manager")
    settings.setDefaultFormat(1)
    settings.beginGroup('main')
    value = settings.value(name, None)
    return value


def clear_layout(layout):
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)

        if isinstance(item, QtGui.QWidgetItem):
            item.widget().close()
        elif isinstance(item, QtGui.QSpacerItem):
            pass
        else:
            clear_layout(item.layout())

        layout.removeItem(item) 
    return True


def set_row_style(row):
    """
    Style the new row based on the row status and then return it
    """
    #Gets the first digit from priority for the priority code
    code = int(row.priority.text().left(1))
    font = row.font()
    #If the job is running, make the font bold and disable the start button
    if row.running != '0':
        font.setBold(True)
        row.edit_job.setEnabled(False)
        row.hide_job.setEnabled(False)
    #If the job is finished, make the font italic, disable the row and
    #set the background to dark gray
    if row.finished != '0':
        font.setItalic(True)
        row.setStyleSheet('background-color: rgb(55,55,55);')
    #If the job is being modified, strike out the font and disable the row
    if row.modifying != '0':
        font.setStrikeOut(True)

    #Apply the new style font
    row.hide_job.setFont(font)
    row.job_number.setFont(font)
    row.material.setFont(font)
    row.material_qty.setFont(font)
    row.notes.setFont(font)
    row.priority.setFont(font)
    row.edit_job.setFont(font)

    #Use the color dict to get the correct priority color code
    color = colors[code].getRgb()
    color_style = 'background-color: rgb({0},{1},{2});'.format(*color)
    row.priority.setStyleSheet(color_style)

    #Return the newly styled row to be added to the Gui
    return row


class MaterialCompleter(QtGui.QCompleter):
    """
    Creates a completer to use on the material line
    """
    def __init__(self, parent=None):
        QtGui.QCompleter.__init__(self, parent)
        qry = QtSql.QSqlQuery()
        data = ("Select material from Work_Orders_tbl group by material order "
                "by material")
        if qry.exec_(data):
            mod = QtSql.QSqlQueryModel()
            mod.setQuery(qry)
            self.setModel(mod)
        else:
            db_err(qry)


class NewRow(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setMaximumHeight(77)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setStyleSheet("background-color: rgb(225, 225, 225); border-color: rgb(230, 230, 230);")
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Plain)
        self.setLineWidth(1)
        self.upload_pdf = QtGui.QPushButton(self)
        init_format(self.upload_pdf, align=None, icon=QtGui.QIcon(":/icons/upload.png"))
        self.hide_job = QtGui.QPushButton("Hide Job", self)
        init_format(self.hide_job, max_size=None, min_size=None, align=None, flat=None,
                    style="border-width:0px;background-color: rgb(255, 255, 255);")
        self.edit_job = QtGui.QPushButton("Edit Job", self)
        init_format(self.edit_job, max_size=None, min_size=None, align=None, flat=None,
                    style="border-width:0px;background-color: rgb(255, 255, 255);")
        self.material_qty = QtGui.QLineEdit(self)
        init_format(self.material_qty, max_size=QtCore.QSize(75, 24), flat=False)
        self.material_qty.setFrame(False)
        self.job_number = QtGui.QLineEdit(self)
        init_format(self.job_number, max_size=QtCore.QSize(150, 24), flat=False)
        self.job_number.setFrame(False)
        self.material = QtGui.QLineEdit(self)
        init_format(self.material, max_size=None, min_size=None, flat=False)
        self.material.setFrame(False)
        self.priority = QtGui.QLineEdit(self)
        init_format(self.priority, flat=False)
        self.print_report = QtGui.QPushButton(self)
        init_format(self.print_report, align=None, icon=QtGui.QIcon(":/icons/printer.png"))
        self.label = QtGui.QLabel("Qty", self)
        init_format(self.label, flat=False)
        self.notes = QtGui.QPlainTextEdit(self)
        init_format(self.notes, max_size=QtCore.QSize(1200, 50), align=None, flat=None)
        self.line = QtGui.QFrame(self)
        self.line.setStyleSheet("color: rgb(255, 255, 255);")
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        layout = QtGui.QGridLayout(self)
        layout.setContentsMargins(6, 4, 6, 5)
        layout.setHorizontalSpacing(12)
        layout.addWidget(self.upload_pdf, 0, 3, 2, 1)
        layout.addWidget(self.hide_job, 0, 7, 2, 1)
        layout.addWidget(self.edit_job, 0, 6, 2, 1)
        layout.addWidget(self.material, 0, 4, 1, 2)
        layout.addWidget(self.material_qty, 1, 5)
        layout.addWidget(self.job_number, 0, 1, 2, 1)
        layout.addWidget(self.priority, 0, 0, 2, 1)
        layout.addWidget(self.print_report, 0, 2, 2, 1)
        layout.addWidget(self.label, 1, 4, 1, 1)
        layout.addWidget(self.notes, 0, 8, 2, 1)
        layout.addWidget(self.line, 2, 0, 1, 9)


def init_format(widget, max_size=QtCore.QSize(75, 50), min_size=QtCore.QSize(50, 24), icon=None,
                align=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter), flat=True,
                style="border-width:0px;"):
    print "Setting Max"
    if max_size:
        widget.setMaximumSize(max_size)
    print "Setting Min"
    if min_size:
        widget.setMinimumSize(min_size)
    print "Setting Align"
    if align:
        widget.setAlignment(align)
    print "Setting Min"
    if icon:
        widget.setIcon(QtGui.QIcon(icon))
    if style:
        widget.setStyleSheet(style)
    if flat:
        widget.setFlat(True)