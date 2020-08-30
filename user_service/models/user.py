# id = Column(sqlalchemy.Integer, primary_key=True)  # SET TO UUID???
# licence_id = Column(Integer, nullable=False)
# username = Column(String(150), nullable=False)
# password = Column(String(128), nullable=False)
# is_admin = Column(Boolean, default=False),
# first_name = Column(String(30), nullable=False)
# last_name = Column(String(150), nullable=False)
# email = Column(String(120), nullable=False, unique=True)
# phone_number = Column(String(12), default=None)
# address = Column(String(100), default=None)
# position = Column(String(30), nullable=False)
# last_login = Column(DateTime, nullable=False, default=datetime.now())
# date_joined = Column(DateTime, nullable=False, default=datetime.now())
# is_active = Column(Boolean, default=True)
# groups

class UserTO:
    def __init__(self, id, licence_id, username, password, email, is_admin, first_name, last_name, phone_number,
                 address, position, last_login, date_joined, is_active, groups=None):
        self.id = id
        self.licence_id = licence_id
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.position = position
        self.last_login = last_login
        self.date_joined = date_joined
        self.is_active = is_active
        self.groups = groups or []

    def add_group(self, group_to):
        self.groups.append(group_to)
