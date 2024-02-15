
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
        section1ButtonsLayout.addWidget(QPushButton("Найти"))
        section1ButtonsLayout.addWidget(QPushButton("Добавить"))
        section1ButtonsLayout.addWidget(QPushButton("Удалить"))
        section1.addLayout(section1ButtonsLayout)
        tab1Layout.addLayout(section1)

        # Second Section
        section2 = QVBoxLayout()
        textFields = [QLineEdit() for _ in range(6)]
        for textField in textFields:
            section2.addWidget(textField)
        wearRateButton = QPushButton('Степень износа')
        wearRateButton.clicked.connect(self.showWearRateWindow)
        section2.addWidget(wearRateButton)

        section2ButtonsLayout = QHBoxLayout()
        section2ButtonsLayout.addWidget(QPushButton("Редактировать"))
        section2ButtonsLayout.addWidget(QPushButton("Сохранить"))
        section2.addLayout(section2ButtonsLayout)
        tab1Layout.addLayout(section2)

    def showWearRateWindow(self):
        self.wearRateWindow = WearRateWindow()
        self.wearRateWindow.show()

if __name__ == '__main__':
    app = QApplication([]) 
    window = MyApp()
    window.show()
    app.exec()
