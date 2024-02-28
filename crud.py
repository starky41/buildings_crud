from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView, QScrollArea, QGridLayout
from database import engine, db_session
from data_access_layer import DataAccessLayer
from PyQt6.QtGui import QIcon
from get_model_class import get_model_class
from crud_operations import CrudOperations



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

            # Create a QGridLayout for the line edits and labels
            grid_layout = QGridLayout()
            row = 0
            column = 0
            for column_index, column in enumerate(columns):
                if column.primary_key and column.autoincrement:
                    continue  # Skip creating LineEdits for autoincrement fields
                label = QLabel(column.name)
                line_edit = QLineEdit()
                # Adjust the row based on the presence of primary keys
                row_offset = sum(1 for col in primary_key_columns if col != column.name)
                grid_layout.addWidget(label, row + row_offset, column_index % 2 * 2)  
                grid_layout.addWidget(line_edit, row + row_offset, column_index % 2 * 2 + 1) 
                if (column_index + len(primary_key_columns)) % 2 == 1:
                    row += 1  # Move to the next row after two columns

            # Add the QGridLayout to a scroll area for editing fields
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_widget.setLayout(grid_layout)
            scroll_area.setWidget(scroll_widget)
            self.layout.addWidget(scroll_area)

            save_button = QPushButton("Создать")
            self.crud_operations = CrudOperations()
            save_button.clicked.connect(lambda: self.crud_operations.createItem(self.model_class_name, db_session, DataAccessLayer, CrudOperations.refreshTable, CrudOperations.clearLineEdits, self.table_widget, CrudOperations.addUpdateButton, self.layout))
            self.layout.addWidget(save_button)

            # Create a QTableWidget to display the database table data
            self.table_widget = QTableWidget()
            self.layout.addWidget(self.table_widget)

            # Resize columns to fit content
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

            # Load data into the table widget
            self.crud_operations.refreshTable(self.model_class_name, self.table_widget, CrudOperations.addUpdateButton)

            # Allow users to interactively resize columns
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

            # Add a Refresh button to reload the data
            refresh_button = QPushButton("Обновить")
            refresh_button.clicked.connect(lambda: CrudOperations.refreshTable(self, self.model_class_name, self.table_widget, CrudOperations.addUpdateButton))
            self.layout.addWidget(refresh_button)

            # Add a Delete button with an icon
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("icons/trashbin.png"))
            delete_button.clicked.connect(lambda: CrudOperations.deleteSelectedItems(self, self.table_widget, self.model_class_name, db_session, CrudOperations.refreshTable))
            self.layout.addWidget(delete_button)

            update_button = QPushButton("Изменить")
            update_button.clicked.connect(lambda: CrudOperations.handleUpdateButtonClick(self, CrudOperations.updateItem, self.model_class_name, self.table_widget))
            self.layout.addWidget(update_button)

            self.setLayout(self.layout)




    def configureMainWindow(self):
        self.resize(640, 480)





