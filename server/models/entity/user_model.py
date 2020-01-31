from server import db


users_groups = db.Table('users_groups', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    licence_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    phone_number = db.Column(db.String(12), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    position = db.Column(db.String(30), nullable=True)
    groups = db.relationship('Group', secondary=users_groups, lazy='select',
                             backref=db.backref('users', lazy='subquery'))

    def __init__(self, licence_id, username, password_hash, email, is_admin, phone_number=None, address=None,
                 first_name=None, last_name=None, position=None, groups=[]):
        self.licence_id = licence_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.is_admin = is_admin
        self.phone_number = phone_number
        self.address = address
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.groups = []

    def __repr__(self):
        return '[{}] <{}. {}>'.format(self.licence_id, self.id, self.username)
