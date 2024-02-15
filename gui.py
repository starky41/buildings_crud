
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QWidget, QTabWidget)

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

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout()
        centralWidget.setLayout(layout)

        tabWidget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()  # Placeholder for the second tab
        tabWidget.addTab(tab1, "Поиск")
        tabWidget.addTab(tab2, "Справочник")
        layout.addWidget(tabWidget)

        tab1Layout = QHBoxLayout()
        tab1.setLayout(tab1Layout)

        # First Section
        section1 = QVBoxLayout()
        section1.addWidget(QLabel("Поиск"))
        streetLayout = QHBoxLayout()
        streetLabel = QLabel("Улица")
        streetLineEdit = QLineEdit()
        streetLayout.addWidget(streetLabel)
        streetLayout.addWidget(streetLineEdit)
        section1.addLayout(streetLayout)

        buildingNrLayout = QHBoxLayout()
        buildingNrLabel = QLabel("Номер")
        buildingNrLineEdit = QLineEdit()
        buildingNrLayout.addWidget(buildingNrLabel)
        buildingNrLayout.addWidget(buildingNrLineEdit)
        section1.addLayout(buildingNrLayout)

        section1ButtonsLayout = QHBoxLayout()
        findButton = QPushButton("Найти")
        findButton.clicked.connect(self.showFindResults)
        addButton = QPushButton("Добавить")
        addButton.clicked.connect(self.showAdditionFields)
        section1ButtonsLayout.addWidget(findButton)
        section1ButtonsLayout.addWidget(addButton)
        section1ButtonsLayout.addWidget(QPushButton("Удалить"))
        section1.addLayout(section1ButtonsLayout)
        tab1Layout.addLayout(section1)

        # Second Section (Initially hidden)
        self.section2Wrapper = QWidget()  # Wrapper to control visibility
        self.section2 = QVBoxLayout()
        self.section2Wrapper.setLayout(self.section2)
        self.textFields = [QLineEdit() for _ in range(6)]
        self.section2Widgets = self.textFields  # Store reference to add/remove later
        self.wearRateButton = QPushButton('Степень износа')
        self.wearRateButton.clicked.connect(self.showWearRateWindow)
        self.section2.addWidget(self.wearRateButton)

        self.section2ButtonsLayout = QHBoxLayout()
        self.section2ButtonsLayout.addWidget(QPushButton("Редактировать"))
        self.section2ButtonsLayout.addWidget(QPushButton("Сохранить"))
        self.section2.addLayout(self.section2ButtonsLayout)
        tab1Layout.addWidget(self.section2Wrapper)
        self.section2Wrapper.setVisible(False)  # Start with the section hidden

    def showFindResults(self):
        # Clear the second section and show a label with some text
        for widget in self.section2Widgets:
            self.section2.removeWidget(widget)
            widget.deleteLater()
        self.section2Widgets = [QLabel("Results of the search will be displayed here.")]
        for widget in self.section2Widgets:
            self.section2.addWidget(widget)
        self.section2Wrapper.setVisible(True)

    def showAdditionFields(self):
        # Clear the second section and add the text fields
        for widget in self.section2Widgets:
            self.section2.removeWidget(widget)
            widget.deleteLater()
        self.section2Widgets = [QLineEdit() for _ in range(6)]
        for widget in self.section2Widgets:
            self.section2.addWidget(widget)
        self.section2Wrapper.setVisible(True)

    def showWearRateWindow(self):
        self.wearRateWindow = WearRateWindow()
        self.wearRateWindow.show()


