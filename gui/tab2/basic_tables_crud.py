from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHeaderView
from database.database import db_session
from database.get_model_class import get_model_class
from database.crud_operations import CrudOperations
from ..widgets.sortable_table_widget import SortableTableWidget
class CrudWindow(QWidget):
    def __init__(self, model_class_name):
        super().__init__()
        self.model_class_name = model_class_name
        self.initUI()

    def initUI(self):
        self.configureMainWindow()
        self.setWindowTitle(f"CRUD for {self.model_class_name}")
        self.layout = QVBoxLayout()

        model_class = get_model_class(self.model_class_name)
        if model_class:
            # Get the columns of the model table
            columns = model_class.__table__.columns
            primary_key_columns = [col.name for col in model_class.__table__.primary_key]
            for column in columns:
                if column.primary_key and column.autoincrement:
                    continue  # Skip creating LineEdits for autoincrement fields
                label = QLabel(column.name)
                line_edit = QLineEdit()
                self.layout.addWidget(label)
                self.layout.addWidget(line_edit)
        
            save_button = QPushButton("Создать")
            # Create an instance of CrudOperations
            self.crud_operations = CrudOperations(db_session)
            save_button.clicked.connect(lambda: self.crud_operations.createItem(self.model_class_name, self.table_widget, self.layout))
            self.layout.addWidget(save_button)
        
            # Create a QTableWidget to display the database table data
            self.table_widget = SortableTableWidget()
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.layout.addWidget(self.table_widget)

            # Add a Refresh button to reload the data
            # refresh_button = QPushButton("Обновить")
            # refresh_button.clicked.connect(lambda: CrudOperations.refreshTable(self, self.model_class_name, self.table_widget, CrudOperations.addUpdateButton))
            # self.layout.addWidget(refresh_button)

            # Add a Delete button with an icon
            delete_button = QPushButton("Удалить")
            # delete_button.setIcon(QIcon("icons/trashbin.png"))
            delete_button.clicked.connect(lambda: CrudOperations.deleteSelectedItems(self, self.table_widget, self.model_class_name))
            self.layout.addWidget(delete_button)

            update_button = QPushButton("Изменить")
            # update_button.clicked.connect(lambda: self.handleUpdateButtonClick())
            update_button.clicked.connect(lambda: CrudOperations.handleUpdateButtonClick(self, self.model_class_name, self.table_widget))
            self.layout.addWidget(update_button)

        
            self.setLayout(self.layout)
            self.crud_operations.refreshTable(self.model_class_name, self.table_widget)


    def configureMainWindow(self):
        self.resize(640, 480)





