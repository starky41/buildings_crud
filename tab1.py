from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QGridLayout
from show_additional_fields import show_additional_fields
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
            show_additional_fields(self, True)
            print("Add button clicked and action executed once")
        else:
            self.addButtonClicked = False
            show_additional_fields(self, False)

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

