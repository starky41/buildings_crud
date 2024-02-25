from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QGridLayout
from PyQt6.QtGui import QIntValidator, QDoubleValidator
class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.addButtonClicked = False
        self.section2_widgets = []
        self.initUI()

    def initUI(self):
        tab1Layout = QHBoxLayout()
        self.setLayout(tab1Layout)
        self.setupTab1SearchSection(tab1Layout)
        self.setupTab1SecondSection(tab1Layout)

    def setupTab1SearchSection(self, layout):
        from PyQt6.QtCore import Qt
        section1 = QVBoxLayout()
        section1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        section1.addWidget(QLabel("Поиск"))
        self.addSearchField("Улица", section1)
        self.addSearchField("Номер", section1)
        self.addSection1Buttons(section1)
        layout.addLayout(section1)

    def addSearchField(self, label, layout):
        fieldLayout = QHBoxLayout()
        fieldLabel = QLabel(label)
        fieldLineEdit = QLineEdit()
        fieldLayout.addWidget(fieldLabel)
        fieldLayout.addWidget(fieldLineEdit)
        layout.addLayout(fieldLayout)

    def addSection1Buttons(self, layout):
        section1ButtonsLayout = QHBoxLayout()
        findButton = QPushButton("Найти")
        findButton.clicked.connect(self.showFindResults)
        addButton = QPushButton("Добавить")
        addButton.clicked.connect(self.addFunction)
        section1ButtonsLayout.addWidget(findButton)
        section1ButtonsLayout.addWidget(addButton)
        section1ButtonsLayout.addWidget(QPushButton("Удалить"))
        layout.addLayout(section1ButtonsLayout)

    def setupTab1SecondSection(self, layout):
        self.section2 = QVBoxLayout()
        section2ButtonsLayout = QHBoxLayout()
        section2ButtonsLayout.addWidget(QPushButton("Редактировать"))
        section2ButtonsLayout.addWidget(QPushButton("Сохранить"))
        self.section2.addLayout(section2ButtonsLayout)
        self.section2Wrapper = QWidget()
        self.section2Wrapper.setLayout(self.section2)
        layout.addWidget(self.section2Wrapper)
        self.section2Wrapper.setVisible(False)

    def addFunction(self):
        if not self.addButtonClicked:
            self.addButtonClicked = True
            self.showAdditionFields(True)
            print("Add button clicked and action executed once")
        else:
            self.addButtonClicked = False
            self.showAdditionFields(False)

    def showFindResults(self):
        try:
            for widget in self.section2_widgets:
                self.section2.removeWidget(widget)
                widget.deleteLater()
            self.section2_widgets = [QLabel("Results of the search will be displayed here.")]

            for widget in self.section2_widgets:
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