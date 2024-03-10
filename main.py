from database.database import init_db, db_session
from database.data_access_layer import DataAccessLayer
from gui.gui import MyApp
from PyQt6.QtWidgets import QApplication

init_db()

dal = DataAccessLayer(db_session)

def main():
    print("")

if __name__ == "__main__":
    
    main()
    app = QApplication([]) 
    window = MyApp()
    window.show()
    app.exec()
    