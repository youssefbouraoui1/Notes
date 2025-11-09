from dtos import CreateUserRequest
from models import User


def createUser(user_dto: CreateUserRequest):
    user = User(first_name=user_dto.first_name,
        last_name=user_dto.last_name,
        email=user_dto.email)
    
    user.set_password(user_dto.password) # this will hash password
    
    user.save()
    
    return UserSerializer(user).data
    