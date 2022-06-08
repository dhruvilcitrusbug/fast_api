from fastapi import FastAPI, Depends
from users import fetch_users, fetch_user_id, fetch_user_email, create_user, create_user_profile
from users import UserValidator, UserDataValidator
from users_models import UsersSignUp
from commons import as_dict
from oauths import oauth2_scheme

app = FastAPI()


@app.get("/users")
async def list_users():

    return {"data": fetch_users()}


@app.get("/user/{user_id}")
async def user_detail(user_id: int):
    return {"data": fetch_user_id(user_id)}


@app.post("/user")
async def user_create(data: UsersSignUp):
    data = as_dict(data)
    user_data = data.copy()
    user_profile = user_data.pop("data", {})
    company = user_data.pop("company", {})
    invitation_company = user_data.pop("invitation_company", False)
    user = fetch_user_email(user_email=user_data.get("email"))
    if not user:
        try:
            valid_data = UserValidator(**user_data)
            user_id = create_user(valid_data)
            user_data_valid_data = UserDataValidator(user_id=user_id, **user_profile)
            create_user_profile(user_data_valid_data)
            return {"data": fetch_user_id(user_id)}
        except TypeError as e:
            print(e)
            return {"data": "missing required data"}
    else:
        return {"data": "User with this email already exits"}
