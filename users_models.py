from pydantic import BaseModel


class UsersSignUp(BaseModel):
    """
    This is a value object that should be used to validate User Register Data
    """

    data: dict = {
        'first_name': "string",
        'last_name': "string",
        'mobile': "string"
    }
    email: str
    password: str
