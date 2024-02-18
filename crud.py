from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, BuildingRoof, BuildingFloor, Facade, BuildingDescription, WearRate
from database import engine, db_session
from data_access_layer import DataAccessLayer

class CrudWindow(QWidget):
    def __init__(self, model_class_name):
        super().__init__()
        self.model_class_name = model_class_name
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"CRUD for {self.model_class_name}")
        self.layout = QVBoxLayout()

        model_class = get_model_class(self.model_class_name)
        if model_class:
            # Get the columns of the model table
            columns = model_class.__table__.columns.keys()
            for column in columns:
                label = QLabel(str(column))
                line_edit = QLineEdit()
                self.layout.addWidget(label)
                self.layout.addWidget(line_edit)

            save_button = QPushButton("Save")
            save_button.clicked.connect(self.createItem)
            self.layout.addWidget(save_button)

        
            # Create a QTableWidget to display the database table data
            self.table_widget = QTableWidget()
            self.layout.addWidget(self.table_widget)

            # Add a Refresh button to reload the data
            refresh_button = QPushButton("Refresh")
            refresh_button.clicked.connect(self.refreshTable)
            self.layout.addWidget(refresh_button)

            self.setLayout(self.layout)
            self.refreshTable()

        self.setLayout(self.layout)
    def refreshTable(self):
        model_class = get_model_class(self.model_class_name)
        if model_class:
            # Clear existing data in the table widget
            self.table_widget.clear()

            # Fetch data from the database table
            with engine.connect() as connection:
                result = connection.execute(model_class.__table__.select())
                rows = result.fetchall()

            # Set the table dimensions based on the retrieved data
            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(model_class.__table__.columns))

            # Populate the table with the fetched data
            for row_idx, row in enumerate(rows):
                for col_idx, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.table_widget.setItem(row_idx, col_idx, item)

            # Set table headers
            headers = [str(col) for col in model_class.__table__.columns.keys()]
            self.table_widget.setHorizontalHeaderLabels(headers)

    from data_access_layer import DataAccessLayer


    def createItem(self):
        model_class = get_model_class(self.model_class_name)
        if model_class:
            data = self.getFormData(columns=model_class.__table__.columns.keys())
            new_instance = model_class(**data)
            dal = DataAccessLayer(db_session)
            dal.create(new_instance)

    def getFormData(self, columns):
        data = {}
        for i in range(0, len(columns)):
            label = self.layout.itemAt(i * 2).widget()
            line_edit = self.layout.itemAt((i * 2) + 1).widget()
            data[label.text()] = line_edit.text()
        return data
    
from models import Street, TypeConstruction

def get_model_class(model_class_name):
    model_mapping = {
        'Street': Street,
        'TypeConstruction': TypeConstruction,
        'BasicProject': BasicProject,
        'Appointment': Appointment,
        'LoadBearingWalls': LoadBearingWalls,
        'BuildingRoof': BuildingRoof,
        'BuildingFloor': BuildingFloor,
        'Facade': Facade,
        'BuildingDescription': BuildingDescription,
        'WearRate': WearRate
        # Add more model mappings as needed
    }
    return model_mapping.get(model_class_name)