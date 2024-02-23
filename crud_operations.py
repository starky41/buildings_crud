from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from PyQt6.QtWidgets import QMessageBox
from data_access_layer import DataAccessLayer
from database import engine, db_session
class CrudOperations:

    def createItem(self, model_class_name, db_session, get_model_class, getFormData, DataAccessLayer, refreshTable, clearLineEdits):
        model_class = get_model_class(model_class_name)
        if model_class:
            inspector = inspect(model_class)
            columns = [column.name for column in inspector.columns]
            try:
                data = getFormData(columns=columns, model_class=model_class)
                new_instance = model_class(**data)
                dal = DataAccessLayer(db_session)
                dal.create(new_instance)
            except ValueError as e:
                self.showErrorDialog(str(e))
                db_session.rollback()
            except IntegrityError:
                self.showErrorDialog("The value already exists in the database")
                db_session.rollback()
            else:
                refreshTable()
                clearLineEdits(columns)
    

    def deleteSelectedItems(self, data_widget, model_class_name, db_session, get_model_class):
        dal = DataAccessLayer(db_session)
        selected_rows = data_widget.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(data_widget, "No selection", "Please select the rows you want to delete.")
            return

        model_class = get_model_class(model_class_name)
        if model_class:
            table_obj = model_class.__table__
            primary_key_columns = [col.name for col in table_obj.primary_key]
            with engine.connect() as connection:
                for idx in sorted(selected_rows, reverse=True):
                    row_data = [data_widget.table_widget.item(idx.row(), col).text() for col in range(data_widget.table_widget.columnCount())]
                    identifier = {col: val for col, val in zip(primary_key_columns, row_data)}
                    try:
                        # Use the delete method from the data access layer
                        dal.delete(model_class, **identifier)
                        data_widget.table_widget.removeRow(idx.row())
                    except IntegrityError as e:
                        QMessageBox.critical(data_widget, "Error", f"An error occurred while deleting the record: {e}")

                data_widget.refreshTable()



    def showErrorDialog(self, message):
        # Code to create and display an error dialog with the given message
        error_dialog = QMessageBox()
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()