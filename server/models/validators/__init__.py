from .user_schemas import CreateUserSchema, LoginUserSchema, SetPasswordUserSchema, SetUserDataSchema


login_validator = LoginUserSchema()
create_user_validator = CreateUserSchema()
set_user_password_validator = SetPasswordUserSchema()
set_user_data_validator = SetUserDataSchema()
