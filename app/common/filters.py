from flask import g
import typing


class CurrentUser:
    def __init__(self, user_id, user_role, user_name, user_groups: typing.List):
        self.user_id = user_id
        self.user_role = user_role
        self.user_name = user_name
        self.user_groups = user_groups


class QueryByRoleMixin:
    def filter_by_role(self, q, params=None):
        """
        DON'T CHANGE 'params' IN CALLBACK FUNCTIONS
        """
        role = self.get_current_role()
        _q = None

        manager = getattr(self, 'filter_by_manager', None)
        if role == '管理员' and callable(manager):
            _q = manager(q, params)

        reviewer = getattr(self, 'filter_by_reviewer', None)
        if role == '审核员' and callable(reviewer):
            _q = reviewer(q, params)

        annotator = getattr(self, 'filter_by_annotator', None)
        if role == '标注员' and callable(annotator):
            _q = annotator(q, params)

        return _q or q

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
