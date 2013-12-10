__author__ = 'rhanson'
from PyQt4 import QtSql, QtGui
import sys
from dbConnection import db_err

work_schedule = 'Select * from {0}workSchedule_qry'
work_order_pdf_check = "Select job_Id from workOrderPDF where job_Id={0}"
finish_work_order = "Update Work_Orders_tbl set `show`=0 where Job_ID = {0}"
modify_work_order = "Update Work_Orders_tbl set modifying=if(modifying=0,1,0) where Job_ID = {0}"
update_work_order = "Update Work_Orders_tbl Set priority={1},material='{2}',materialQty={3} where Job_ID={0}"
insert_pdf = "Replace into workOrderPDF (job_Id, report_file) VALUES({0}, 0x{1})"
get_pdf = "Select file from workOrderPDF where job_Id = {0}"
report_header_data = ("Select Job_num, date_Format(JDate, '%Y-%m-%d'), Machine_Desc from Work_Orders_tbl join "
                      "Machine_tbl on Work_Orders_tbl.Machine_ID = Machine_tbl.Machine_ID Where Job_ID = {0}")
report_data = ("Select `Part Num`, `Qty`, `Desc`, `Mat`, `Process`, `Dest`, `Notes`, `Print`, "
               "`Hot`, `Order`, `Tracking` from workOrderData_qry Where Job_ID = {0}")


def query(data, args=None, db='qt_sql_default_connection'):
    qry = QtSql.QSqlQuery(db)
    try:
        data = getattr(sys.modules[__name__], data)
    except AttributeError:
        QtGui.QMessageBox.critical(None, "Query Not Found", "A query matching %s was not found. Typo?" % data)
        return False
    if args:
        data = data.format(*args)
    if qry.exec_(data):
        return qry
    else:
        db_err(qry)
        return False