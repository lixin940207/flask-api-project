# coding=utf-8
# @Author: James Gu
# @Date: 2020/3/12
import abc


class BaseModel:

    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def get_by_id(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def get_by_filter(self, **kwargs):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def create(self, entity):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def bulk_create(self, entity_list):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def delete(self, _id):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def bulk_delete(self, _id_list):
        raise NotImplementedError("Method not implemented.")

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def update(self, entity):
        raise NotImplementedError("Method not implemented.")
