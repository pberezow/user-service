class AbstractTO:
    __name__ = 'AbstractTO'

    def __init__(self, model):
        pass

    @classmethod
    def from_list(cls, model_list):
        objects = []
        for obj in model_list:
            objects.append(cls(obj))
        return objects

    def to_dict(self):
        raise NotImplementedError()

    def set_data(self, form):
        for key in form:
            if not hasattr(self, key):
                return f'Object {self.__name__} has no {key} attribute'
            setattr(self, key, form[key])

    def update_model(self, model):
        for key in self.__dict__:
            if not hasattr(model, key):
                return f'Table {model.__tablename__} has no {key} field'
            setattr(model, key, getattr(self, key))
