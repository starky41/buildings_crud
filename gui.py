
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QWidget, QTabWidget, QGridLayout)
from PyQt6.QtGui import QIntValidator, QDoubleValidator


class WearRateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wear Rate')
        # Initialize UI components for Wear Rate Window here
        # ...

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Application')
        self.initUI()
        self.section2Widgets = []  # Define section2Widgets as an empty list

    def initUI(self):
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout()
        centralWidget.setLayout(layout)
        self.resize(800, 600)
        tabWidget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()  # Placeholder for the second tab
        tabWidget.addTab(tab1, "Поиск")
        tabWidget.addTab(tab2, "Справочник")
        layout.addWidget(tabWidget)

        tab1Layout = QHBoxLayout()
        tab1.setLayout(tab1Layout)

        # First Section
        self.section1 = QVBoxLayout()
        self.section1.addWidget(QLabel("Поиск"))
        streetLayout = QHBoxLayout()
        streetLabel = QLabel("Улица")
        streetLineEdit = QLineEdit()
        streetLayout.addWidget(streetLabel)
        streetLayout.addWidget(streetLineEdit)
        self.section1.addLayout(streetLayout)

        buildingNrLayout = QHBoxLayout()
        buildingNrLabel = QLabel("Номер")
        buildingNrLineEdit = QLineEdit()
        buildingNrLayout.addWidget(buildingNrLabel)
        buildingNrLayout.addWidget(buildingNrLineEdit)
        self.section1.addLayout(buildingNrLayout)

        self.section1ButtonsLayout = QHBoxLayout()
        findButton = QPushButton("Найти")
        findButton.clicked.connect(self.showFindResults)
        self.addButton = QPushButton("Добавить", self)
        self.addButton.clicked.connect(self.addFunction)

        centralWidget = QWidget()

        self.section1ButtonsLayout.addWidget(findButton)
        self.section1ButtonsLayout.addWidget(self.addButton)
        self.section1ButtonsLayout.addWidget(QPushButton("Удалить"))
        self.section1.addLayout(self.section1ButtonsLayout)
        tab1Layout.addLayout(self.section1)

        # Second Section
        self.section2 = QVBoxLayout()
        tab2.setLayout(self.section2)

        self.section2ButtonsLayout = QHBoxLayout()
        self.section2ButtonsLayout.addWidget(QPushButton("Редактировать"))
        self.section2ButtonsLayout.addWidget(QPushButton("Сохранить"))
        self.section2.addLayout(self.section2ButtonsLayout)

        self.section2Wrapper = QWidget()
        self.section2Wrapper.setLayout(self.section2)
        tab1Layout.addWidget(self.section2Wrapper)
        self.section2Wrapper.setVisible(False)  # Start with the section hidden

        self.addButtonClicked = False

    def addFunction(self):
        if not self.addButtonClicked:
            self.addButtonClicked = True
            self.showAdditionFields(True)
            print("Add button clicked and action executed once")
        elif self.addButtonClicked:
            self.addButtonClicked = False
            self.showAdditionFields(False)


    
    def showFindResults(self):
        # Clear the second section and show a label with some text
        try: 
            for widget in self.section2Widgets:
                self.section2.removeWidget(widget)
                widget.deleteLater()
            self.section2Widgets = [QLabel("Results of the search will be displayed here.")]
        
            for widget in self.section2Widgets:
                self.section2.addWidget(widget)
        except RuntimeError:
            pass
        self.section2Wrapper.setVisible(True)

    def showAdditionFields(self, visibility):
        if not hasattr(self, 'fields_created'):
            self.fields_created = False

        if visibility and not self.fields_created:
            labels = [
                ("ID_street", "int"), ("house", "int"), ("building_body", "int"),
                ("latitude", "numeric"), ("longitude", "numeric"), ("year_construction", "int"),
                ("number_floors", "int"), ("number_entrances", "int"), ("number_buildings", "int"),
                ("number_living_quarters", "int"), ("title", "VARCHAR(150)"), ("ID_type_construction", "INT"),
                ("ID_basic_project", "INT"), ("ID_appointment", "INT"), ("seismic_resistance_min", "NUMERIC"),
                ("seismic_resistance_max", "numeric"), ("zone_SMZ_min", "NUMERIC"), ("zone_SMZ_max", "numeric"),
                ("priming", "VARCHAR(150)"), ("ID_load_bearing_walls", "INT"), ("basement_area", "NUMERIC"),
                ("ID_building_roof", "INT"), ("ID_building_floor", "INT"), ("ID_facade", "INT"),
                ("ID_foundation", "INT"), ("azimuth", "VARCHAR(150)"), ("cadastral_number", "INT"),
                ("cadastral_cost", "NUMERIC"), ("year_overhaul", "INT"), ("accident_rate", "VARCHAR(150)"),
                ("ID_management_company", "INT"), ("Land_area", "Numeric"), ("notes", "VARCHAR(150)"),
                ("author", "VARCHAR(150)")
            ]

            # Clear the second section and add the text fields
            for widget in getattr(self, 'section2Widgets', []):
                self.section2.removeWidget(widget)
                widget.deleteLater()

            # Create a GridLayout
            grid_layout = QGridLayout()
            self.textFields = []

            # Add labels and line edits to the grid layout
            for row, (label_text, data_type) in enumerate(labels):
                label = QLabel(label_text)
                if data_type in ["int", "INT"]:
                    line_edit = QLineEdit()
                    line_edit.setValidator(QIntValidator())
                elif data_type in ["numeric", "NUMERIC"]:
                    line_edit = QLineEdit()
                    line_edit.setValidator(QDoubleValidator())
                else:  # Assume VARCHAR(150) or similar string types
                    line_edit = QLineEdit()
                    line_edit.setMaxLength(150)

                # Determine the column by taking the row modulus 2 (for 2 columns)
                column = row % 2
                # Calculate the grid row by integer dividing the label index by 2
                grid_row = row // 2

                grid_layout.addWidget(label, grid_row, column * 2)  # Multiply by 2 for alternating columns
                grid_layout.addWidget(line_edit, grid_row, column * 2 + 1)

                self.textFields.append(line_edit)

            self.section2.addLayout(grid_layout)
            self.fields_created = True

        self.section2Wrapper.setVisible(visibility)

    def showWearRateWindow(self):
        self.wearRateWindow = WearRateWindow()
        self.wearRateWindow.show()



