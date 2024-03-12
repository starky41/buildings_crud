from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from gui.tab2.basic_tables.basic_tables_crud import CrudWindow  # Make sure to import the CrudWindow class
from database.get_model_class import get_model_class

class Tab2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.windows = []
        self.initUI()
        self.tab2Layout = QGridLayout()
        self.setLayout(self.tab2Layout)
        self.tab2Layout.setSpacing(10)

        # Define a mapping between display names and model names
        self.model_name_mapping = {
            "Улица": "Street", 
            "Тип конструкции": "TypeConstruction", 
            "Типовой проект": "BasicProject", 
            "Назначение": "Appointment", 
            "Несущие стены": "LoadBearingWalls", 
            "Крыша": "BuildingRoof", 
            "Перекрытия": "BuildingFloor", 
            "Фасад": "Facade", 
            "Износ": "WearRate"
        }

        for index, display_name in enumerate(self.model_name_mapping.keys()):
            button = QPushButton(display_name)
            button.setFixedSize(150, 40)
            row, col = divmod(index, 3)
            button.clicked.connect(lambda _, name=display_name: self.openCrudWindow(name))
            self.tab2Layout.addWidget(button, row, col)

    def initUI(self):
        pass  # No need for this method as it doesn't add any additional functionality

    def openCrudWindow(self, display_name):
        model_name = self.model_name_mapping.get(display_name)
        model_class = get_model_class(model_name)
        if model_class:
            crud_window = CrudWindow(model_name)  # Pass the model class name as a string
            self.windows.append(crud_window)  # Keep track of the opened windows
            crud_window.show()
        else:
            print(f"Model class for {model_name} not found")

    def addModelButton(self, model_class):
        button = QPushButton(f'Open {model_class.__name__} CRUD')
        button.clicked.connect(lambda: self.openCrudWindow(model_class))
        self.layout().addWidget(button)  # Add the button to Tab2 layout

    def getWearRateButton(self):
        for button in self.findChildren(QPushButton):
            if button.text() == "WearRate":
                return button
        return None
