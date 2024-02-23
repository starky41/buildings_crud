from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from PyQt6.QtWidgets import QMessageBox

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
    
    def showErrorDialog(self, message):
        # Code to create and display an error dialog with the given message
        error_dialog = QMessageBox()
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()