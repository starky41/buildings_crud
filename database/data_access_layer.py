from .database import db_session

class DataAccessLayer:
    def __init__(self, session):
        self.session = session

    def create(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def read(self, model, **kwargs):
        try:
            if kwargs:
                return self.session.query(model).filter_by(**kwargs).all()
            else:
                return self.session.query(model).all()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def update(self, model, identifier, **kwargs):
        try:
            obj = self.session.query(model).filter_by(**identifier).one()
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    raise AttributeError(f"{model.__name__} does not have attribute {key}")
            self.session.commit()
            return obj
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def delete(self, model, **identifier):
        try:
            obj = self.session.query(model).filter_by(**identifier).one()
            self.session.delete(obj)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
