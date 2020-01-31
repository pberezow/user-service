class AbstractTO:
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
