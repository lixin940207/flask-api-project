# coding=utf-8
# @Author: James Gu
# @Date: 2020/3/15
import abc
import unittest


class BaseModelTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @abc.abstractmethod
    def test_get_all(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_get_by_id(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_get_by_filter(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_create(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_bulk_create(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_delete(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_bulk_delete(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_update(self):
        raise NotImplementedError("Method not implemented.")

    @abc.abstractmethod
    def test_bulk_update(self):
        raise NotImplementedError("Method not implemented.")