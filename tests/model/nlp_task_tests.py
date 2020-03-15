# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/15
import unittest
from tests.model.base_model_tests import BaseModelTests
from app.model.nlp_task_model import NlpTaskModel
from app.entity.nlp_task import NlpTask


class NlpTaskModelTests(BaseModelTests):
    def setUp(self) -> None:
        self.nlp_task_model = NlpTaskModel()

    def tearDown(self) -> None:
        pass

    def test_constructor(self) -> None:
        assert type(self.nlp_task_model) == NlpTaskModel

    def test_get_all(self):
        pass

    def test_get_by_id(self):
        mock_nlp_task = NlpTask(nlp_task_name="test_task")
        # self.nlp_task_model.create(mock_nlp_task)
        # print(mock_nlp_task.nlp_task_id)

    def test_get_by_filter(self):
        pass

    def test_create(self):
        pass

    def test_bulk_create(self):
        pass

    def test_delete(self):
        pass

    def test_bulk_delete(self):
        pass

    def test_update(self):
        pass

    def test_bulk_update(self):
        pass


if __name__ == '__main__':
    unittest.main()
