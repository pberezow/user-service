from server import db


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    licence_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    
    def __init__(self, licence_id, name):
        self.licence_id = licence_id
        self.name = name

    def __repr__(self):
        return '<Group: {} [{}]>'.format(self.name, self.licence_id)
