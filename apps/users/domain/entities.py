"""Entities for the users domain"""

from uuid import UUID
from typing import Optional
from datetime import datetime


class User:
    def __init__(
        self,
        id: UUID,
        password: str,
        email: str,
        first_name: str = "",
        last_name: str = "",
        is_active: bool = True,
        is_staff: bool = False,
        is_superuser: bool = False,
        last_login: Optional[datetime] = None,
        date_joined: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_staff = is_staff
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.last_login = last_login
        self.date_joined = date_joined

        # self._validate() # ! TODO: Add validate function

    # def set_password(self, raw_password: str) -> None:
    #     self.password = make_password(raw_password)

    # def check_password(self, raw_password: str) -> bool:
    #     return check_password(raw_password, self.password)
