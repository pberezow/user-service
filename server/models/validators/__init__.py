from .user_schemas import CreateUserSchema, LoginUserSchema, SetPasswordUserSchema, SetUserDataSchema
from .group_schemas import NewGroupSchema, SetGroupDataSchema


login_validator = LoginUserSchema()
create_user_validator = CreateUserSchema()
set_user_password_validator = SetPasswordUserSchema()
set_user_data_validator = SetUserDataSchema()
create_group_validator = NewGroupSchema()
set_group_data_validator = SetGroupDataSchema()
