from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget
from gui.tab2.tab2 import Tab2
from gui.tab1.tab1 import Tab1

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Application')
        self.initUI()
        self.section2Widgets = []  # Define section2Widgets as an empty list
        self.windows = []

    def initUI(self):
        self.setupCentralWidget()
        self.configureMainWindow()
        self.createTabs()

    def setupCentralWidget(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

    def configureMainWindow(self):
        self.resize(800, 600)

    def createTabs(self):
        self.tabWidget = QTabWidget()
        self.tab1 = Tab1()
        self.tab2 = Tab2(self)
        self.tabWidget.addTab(self.tab1, "Поиск")
        self.tabWidget.addTab(self.tab2, "Справочник")
        self.layout.addWidget(self.tabWidget)


    
    




