from PyQt6.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCompleter, QMessageBox, QDialog
from gui.tab1.building_description_dialog import MainWidget
from database.models import Street
from database.database import db_session

class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.addButtonClicked = False
        self.initUI()

    def initUI(self):
        tab1Layout = QVBoxLayout(self)
        self.setLayout(tab1Layout)
        self.setupTab1SearchSection(tab1Layout)
        self.setupTab1SecondSection(tab1Layout)
        self.mainWidget = MainWidget()  # Create an instance of MainWidget
        tab1Layout.addWidget(self.mainWidget)  # Add MainWidget to the layout

    def setupTab1SearchSection(self, layout):
        from PyQt6.QtCore import Qt  # Add this import

        self.section1 = QVBoxLayout()
        self.section1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # self.section1.addWidget(QLabel("Поиск"))
        # self.addSearchField("Улица", self.section1)
        # self.addSearchField("Номер", self.section1)
        #self.addSection1Buttons(self.section1)
        layout.addLayout(self.section1)

    def addSearchField(self, label, layout):
        fieldLayout = QHBoxLayout()
        fieldLabel = QLabel(label)
        fieldLineEdit = QLineEdit()

        if label == "Улица":
            self.setupStreetCompleter(fieldLineEdit)

        fieldLayout.addWidget(fieldLabel)
        fieldLayout.addWidget(fieldLineEdit)
        layout.addLayout(fieldLayout)

    def setupStreetCompleter(self, lineEdit):
        streets = db_session.query(Street).all()
        street_names = [street.street_name for street in streets]
        completer = QCompleter(street_names)
        lineEdit.setCompleter(completer)
        lineEdit.editingFinished.connect(lambda: self.validateStreet(lineEdit, street_names))

    def validateStreet(self, lineEdit, street_names):
        street_entered = lineEdit.text().strip()
        if not street_entered:
            QMessageBox.critical(self, "Error", "Please enter a street name!")
            lineEdit.clear()
            return

        if street_entered not in street_names:
            QMessageBox.critical(self, "Error", "Entered street does not exist!")
            lineEdit.clear()

    # def addSection1Buttons(self, layout):
    #     section1ButtonsLayout = QHBoxLayout()
    #     #findButton = QPushButton("Найти")
    #     #findButton.clicked.connect(self.showFindResults)
    #     # addButton = QPushButton("Таблица")
    #     # Remove the line below
    #     # addButton.clicked.connect(self.addFunction)
    #     #section1ButtonsLayout.addWidget(addButton)
    #     layout.addLayout(section1ButtonsLayout)

    def setupTab1SecondSection(self, layout):
        self.section2Layout = QVBoxLayout()
        self.editButton = QPushButton("Редактировать")
        self.saveButton = QPushButton("Сохранить")
        self.editButton.setVisible(False)
        self.saveButton.setVisible(False)
        self.section2ButtonsLayout = QHBoxLayout()
        self.section2ButtonsLayout.addWidget(self.editButton)
        self.section2ButtonsLayout.addWidget(self.saveButton)
        self.section2Wrapper = QWidget()
        self.section2Wrapper.setLayout(self.section2Layout)
        layout.addWidget(self.section2Wrapper)
        self.section2Wrapper.setVisible(False)
        self.section2Layout.addLayout(self.section2ButtonsLayout)

    # def addFunction(self):
    #     self.additionalFieldsDialog = MainWidget()
    #     self.additionalFieldsDialog.exec()

    def showFindResults(self):
        try:
            results = "Sample results text..."
            self.results_window = ResultsWindow(results)
            self.results_window.exec()
            self.editButton.setVisible(False)
            self.saveButton.setVisible(False)
        except RuntimeError:
            pass

class ResultsWindow(QDialog):
    def __init__(self, results):
        super().__init__()
        self.setWindowTitle("Результаты поиска")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.results_label = QLabel(results)
        layout.addWidget(self.results_label)
        self.editButton = QPushButton("Редактировать")
        self.saveButton = QPushButton("Сохранить")
        self.deleteButton = QPushButton("Удалить")
        layout.addWidget(self.editButton)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.deleteButton)