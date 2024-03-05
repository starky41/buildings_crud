from database.database import init_db, db_session
from database.data_access_layer import DataAccessLayer
from gui.gui import MyApp
from PyQt6.QtWidgets import QApplication
# Initialize the database (create tables if they don't exist)
init_db()

# Instantiate the data access layer with the database session
dal = DataAccessLayer(db_session)

def main():
    from database.models import Appointment
    
    # Usage:
    dal = DataAccessLayer(db_session)
    

    # Create operation example
    # new_appointment = Appointment(appointment_name='test_appointment1')
    # dal.create(new_appointment)

    # Read operation example
    # appointments = dal.read(Appointment)
    # specific_appointment = dal.read(Appointment, ID_appointment=2)

    # # Update operation example
    # dal.update(Appointment, {'ID_building': 1}, house=11)

    # # Delete operation example
    # dal.delete(Appointment, ID_building=1)

if __name__ == "__main__":
    
    main()
    app = QApplication([]) 
    window = MyApp()
    window.show()
    app.exec()
    