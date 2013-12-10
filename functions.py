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
        row.editJob.setEnabled(False)
        row.hideJob.setEnabled(False)
    #If the job is finished, make the font italic, disable the row and
    #set the background to dark gray
    if row.finished != '0':
        font.setItalic(True)
        row.setStyleSheet('background-color: rgb(55,55,55);')
    #If the job is being modified, strike out the font and disable the row
    if row.modifying != '0':
        font.setStrikeOut(True)

    #Apply the new style font
    row.hideJob.setFont(font)
    row.jobNumber.setFont(font)
    row.material.setFont(font)
    row.materialQty.setFont(font)
    row.notes.setFont(font)
    row.priority.setFont(font)
    row.editJob.setFont(font)

    #Use the color dict to get the correct priority color code
    color = colors[code].getRgb()
    colorStyle = 'background-color: rgb({0},{1},{2});'.format(*color)
    row.priority.setStyleSheet(colorStyle)

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