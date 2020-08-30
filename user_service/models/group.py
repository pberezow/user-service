# id = Column(Integer, primary_key=True)
# licence_id = Column(Integer, nullable=False)
# name = Column(String(30), nullable=False)
# users = relationship('User', secondary=users_groups, back_populates='groups')

class GroupTO:
    def __init__(self, id, licence_id, name, users=None):
        self.id = id
        self.licence_id = licence_id
        self.name = name
        self.users = users or []

    def add_user(self, user_to):
        self.users.append(user_to)
