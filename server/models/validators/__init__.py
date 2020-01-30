from .schemas import CreateUserSchema, LoginUserSchema


login_validator = LoginUserSchema()
create_user_validator = CreateUserSchema()
