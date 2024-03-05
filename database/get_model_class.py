from database.models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, BuildingRoof, BuildingFloor, Facade, BuildingDescription, WearRate
def get_model_class(model_class_name):
    model_mapping = {
        'Street': Street,
        'TypeConstruction': TypeConstruction,
        'BasicProject': BasicProject,
        'Appointment': Appointment,
        'LoadBearingWalls': LoadBearingWalls,
        'BuildingRoof': BuildingRoof,
        'BuildingFloor': BuildingFloor,
        'Facade': Facade,
        'BuildingDescription': BuildingDescription,
        'WearRate': WearRate
        # Add more model mappings as needed
    }
    return model_mapping.get(model_class_name)