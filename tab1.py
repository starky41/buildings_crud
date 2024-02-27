from PyQt6.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCompleter
from show_additional_fields import AdditionalFieldsDialog
from models import Street
from database import db_session

class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.addButtonClicked = False
        self.initUI()

    def initUI(self):
        tab1Layout = QVBoxLayout()
        self.setLayout(tab1Layout)
        self.setupTab1SearchSection(tab1Layout)
        self.setupTab1SecondSection(tab1Layout)

    def setupTab1SearchSection(self, layout):
        from PyQt6.QtCore import Qt  # Add this import
        self.section1 = QVBoxLayout()
        self.section1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.section1.addWidget(QLabel("Поиск"))
        self.addSearchField("Улица", self.section1)
        self.addSearchField("Номер", self.section1)
        self.addSection1Buttons(self.section1)
        layout.addLayout(self.section1)

    def addSearchField(self, label, layout):
        fieldLayout = QHBoxLayout()
        fieldLabel = QLabel(label)
        fieldLineEdit = QLineEdit()

        if label == "Улица":
            streets = db_session.query(Street).all()  # Assuming `session` is your SQLAlchemy session
            street_names = [street.street_name for street in streets]
            completer = QCompleter(street_names)
            fieldLineEdit.setCompleter(completer)

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
        self.section2Layout = QVBoxLayout()
        self.editButton = QPushButton("Редактировать")
        self.saveButton = QPushButton("Сохранить")
        self.editButton.setVisible(False)
        self.saveButton.setVisible(False)
        self.section2ButtonsLayout = QHBoxLayout()  # Moved layout creation here
        self.section2ButtonsLayout.addWidget(self.editButton)
        self.section2ButtonsLayout.addWidget(self.saveButton)
        self.section2Wrapper = QWidget()
        self.section2Wrapper.setLayout(self.section2Layout)
        layout.addWidget(self.section2Wrapper)
        self.section2Wrapper.setVisible(False)

    def addFunction(self):
        self.additionalFieldsDialog = AdditionalFieldsDialog()
        self.additionalFieldsDialog.exec()
    def showFindResults(self):
        try:
            # Clear existing widgets in section 2
            for widget in getattr(self, 'section2_widgets', []):
                self.section2Layout.removeWidget(widget)
                widget.deleteLater()

            # Add the "Results of the search" label
            if not hasattr(self, 'results_label'):
                self.results_label = QLabel("Results of the search will be displayed here.")
            self.section2Layout.addWidget(self.results_label)

            # Add the edit and save buttons if not already added
            if self.section2ButtonsLayout not in self.section2Layout.children():
                self.section2Layout.addLayout(self.section2ButtonsLayout)

            # Show the edit and save buttons
            self.editButton.setVisible(True)
            self.saveButton.setVisible(True)
        except RuntimeError:
            pass
        self.section2Wrapper.setVisible(True)