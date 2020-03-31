from flask import g
import typing


class CurrentUser:
    def __init__(self, user_id, user_role, user_name, user_groups: typing.List):
        self.user_id = user_id
        self.user_role = user_role
        self.user_name = user_name
        self.user_groups = user_groups


class CurrentUserMixin:
    @staticmethod
    def get_current_user():
        return CurrentUser(
            user_id=g.user_id,
            user_role=g.user_roles and g.user_roles[0] or "",
            user_name=g.user_name,
            user_groups=g.user_groups
        )

    @staticmethod
    def get_current_role():
        return g.user_roles and g.user_roles[0] or ""

    @staticmethod
    def get_current_user_id():
        return g.user_id
