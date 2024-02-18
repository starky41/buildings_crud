
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, BuildingRoof, BuildingFloor, Facade, BuildingDescription, WearRate


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
            for column in model_class.__table__.columns:
                label = QLabel(str(column.name))
                line_edit = QLineEdit()
                self.layout.addWidget(label)
                self.layout.addWidget(line_edit)

            save_button = QPushButton("Save")
            self.layout.addWidget(save_button)

        self.setLayout(self.layout)

    def createItem(self):
        # Implement the method to create a new instance of the model
        new_instance = self.model_class(**self.getFormData())
        # Save the new_instance to the database or perform necessary actions

    def updateItem(self):
        # Implement the method to update the selected instance of the model
        # Retrieve the instance to update, update its attributes, and save changes
        pass

    def deleteItem(self):
        # Implement the method to delete the selected instance of the model
        # Retrieve the instance to delete and delete it
        pass

    def getFormData(self):
        # Helper method to retrieve data from input fields
        data = {}
        for i in range(1, self.layout.count(), 2):  # Assuming input fields are every 2nd widget
            label = self.layout.itemAt(i).widget()
            line_edit = self.layout.itemAt(i+1).widget()
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