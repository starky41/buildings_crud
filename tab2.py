from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from crud import CrudWindow  # Make sure to import the CrudWindow class
from models import Street, TypeConstruction
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from crud import CrudWindow  # Import the CrudWindow class
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, BuildingRoof, BuildingFloor, Facade, BuildingDescription, WearRate


class Tab2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.windows = []
        self.initUI()
        self.tab2Layout = QGridLayout()
        self.setLayout(self.tab2Layout)
        self.tab2Layout.setSpacing(10)

        buttonNames = [
            "Street", "TypeConstruction", "BasicProject", "Appointment", "LoadBearingWalls", "BuildingRoof", "BuildingFloor", "Facade", "BuildingDescription", "WearRate"  # Add other model names here
        ]

        for index, name in enumerate(buttonNames):
            button = QPushButton(name)
            button.setFixedSize(150, 40)
            row, col = divmod(index, 3)
            button.clicked.connect(lambda _, name=name: self.openCrudWindow(name))
            self.tab2Layout.addWidget(button, row, col)

    def initUI(self):
        pass  # No need for this method as it doesn't add any additional functionality

    def openCrudWindow(self, name):
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
            # Map other model names to their respective classes
        }
        model_class = model_mapping.get(name)
        if model_class:
            crud_window = CrudWindow(name)  # Pass the model class name as a string
            self.windows.append(crud_window)  # Keep track of the opened windows
            crud_window.show()
        else:
            print(f"Model class for {name} not found")


    def addModelButton(self, model_class):
        button = QPushButton(f'Open {model_class.__name__} CRUD')
        button.clicked.connect(lambda: self.openCrudWindow(model_class))
        self.layout().addWidget(button)  # Add the button to Tab2 layout
