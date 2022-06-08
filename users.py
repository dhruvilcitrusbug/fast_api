import hashlib
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate
from db_connect import cursor, conn
from commons import as_dict
from typing import Union
from datetime import datetime, timezone


def make_password(password: str):
    result = hashlib.sha512(password.encode())
    return result.hexdigest()


@dataclass(frozen=True)
class UsersList:
    id: int
    email: str
    user_status: str
    cv_companies_id: int
    cv_company_role_id: int


@dataclass_validate(before_post_init=True)
@dataclass(frozen=True)
class UserValidator:
    """
    This is a value object that should be used to validate User Register Data
    """

    email: str
    password: str


@dataclass_validate(before_post_init=True)
@dataclass(frozen=True)
class UserBasePermissionValidator:
    """
    This is a value object that should be used to validate User Base Permission
    """

    is_active: bool
    is_admin: bool
    user_status: int


@dataclass_validate(before_post_init=True)
@dataclass(frozen=True)
class UserDataValidator:
    """
    This is a value object that should be used to validate User Profile Data
    """

    user_id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    phone: Union[str, None] = None
    mobile: Union[str, None] = None
    address1: Union[str, None] = None
    address2: Union[str, None] = None
    city: Union[str, None] = None
    country: Union[str, None] = None
    postcode: Union[str, None] = None
    mobile_confirmed: bool = False


# (2, 'yivud2105@yopmail.com', '1', None, None)
def fetch_users():
    cursor.execute(
        """select id, email, user_status, cv_companies_id, cv_company_role_id  from cv_users"""
    )
    users = cursor.fetchall()
    users_validated = []
    for user in users:
        user_dict = UsersList(
            id=user[0],
            email=user[1],
            user_status=user[2],
            cv_companies_id=user[3],
            cv_company_role_id=user[4],
        )
        users_validated.append(as_dict(user_dict))
    return users_validated


def fetch_user_id(user_id: int):
    cursor.execute(
        f"""select id, email, user_status, cv_companies_id, cv_company_role_id  from cv_users where cv_users.id={user_id}"""
    )
    user = cursor.fetchone()
    user_dict = as_dict(
        UsersList(
            id=user[0],
            email=user[1],
            user_status=user[2],
            cv_companies_id=user[3],
            cv_company_role_id=user[4],
        )
    )
    return user_dict


def fetch_user_email(user_email: str):
    cursor.execute(
        f"""select id, email, user_status, cv_companies_id, cv_company_role_id  from cv_users where cv_users.email='{user_email}'"""
    )
    user = cursor.fetchone()
    return user


def create_user(
    user_data: UserValidator,
    permission_data: UserBasePermissionValidator = UserBasePermissionValidator(
        is_active=True, is_admin=False, user_status=0
    ),
):
    password_hashed = make_password(user_data.password)
    cursor.execute(
        f"""insert into cv_users (password, email, active, deleted, isadmin, user_status) values ('{password_hashed}', '{user_data.email}', {permission_data.is_active}, {False}, {permission_data.is_admin}, {permission_data.user_status}) RETURNING  id"""
    )
    id_of_new_row = cursor.fetchone()[0]
    conn.commit()
    return id_of_new_row


def create_user_profile(profile_data: UserDataValidator):
    cursor.execute(
        f"""insert into cv_users_data (name, lastname, phone, mobile, address1, address2, city, country, postcode, mobile_confirmed, cv_users_id) values ('{profile_data.first_name}', '{profile_data.last_name}', '{profile_data.phone}', '{profile_data.mobile}', '{profile_data.address1}', '{profile_data.address2}', '{profile_data.city}', '{profile_data.country}', '{profile_data.postcode}', '{profile_data.mobile_confirmed}', '{profile_data.user_id}')"""
    )
    conn.commit()
    return True


