from .abstract_to import AbstractTO


class GroupTO(AbstractTO):
    __name__ = 'GroupTO'

    def __init__(self, group_model):
        super().__init__(group_model)
        self.licence_id = group_model.licence_id
        self.name = group_model.name

    def to_dict(self):
        return {
            'name': self.name
        }
