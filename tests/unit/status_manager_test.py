import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from modules.license.data.status_data import StatusData
from modules.license.exceptions.license_status_fetch_exception import LicenseStatusFetchException
from modules.license.managers.status_manager import StatusManager


class StatusManagerTest(unittest.TestCase):

    @patch("modules.license.data.status_data.StatusData")
    def setUp(self, status_data: StatusData) -> None:
        self.status_data = status_data
        self.status_manager: StatusManager = StatusManager(
            status_data=self.status_data
        )

    def test_get_all_fails_on_missing_statuses(self):
        self.status_data.load_all = MagicMock(return_value=Result(True))
        with self.assertRaises(LicenseStatusFetchException):
            self.status_manager.get_all()
            self.fail("Did not fail on missing license statuses")
        self.status_data.load_all.assert_called_once()

    def test_get_all_caches_on_second_call(self):
        statuses = [{
            "id": 1,
            "const": "STATUS",
            "description": "Status Description"
        }]
        result = Result(True, "", statuses)
        result.set_affected_rows(len(statuses))
        self.status_data.load_all = MagicMock(return_value=result)

        first_called_statuses = self.status_manager.get_all()
        second_called_statuses = self.status_manager.get_all()

        self.status_data.load_all.assert_called_once()
        self.assertEqual(first_called_statuses, second_called_statuses)

    def test_get_by_id_fails_on_invalid_id(self):
        statuses = [{
            "id": 1,
            "const": "STATUS",
            "description": "Status Description"
        }]
        result = Result(True, "", statuses)
        result.set_affected_rows(len(statuses))
        self.status_data.load_all = MagicMock(return_value=result)

        with self.assertRaises(LicenseStatusFetchException):
            self.status_manager.get_by_id(2)
            self.fail("Did not fail on missing status ID")

    def test_get_by_id_caches_on_second_call(self):
        statuses = [{
            "id": 1,
            "const": "STATUS",
            "description": "Status Description"
        }]
        result = Result(True, "", statuses)
        result.set_affected_rows(len(statuses))
        self.status_data.load_all = MagicMock(return_value=result)

        status_first = self.status_manager.get_by_id(1)
        status_second = self.status_manager.get_by_id(1)

        self.status_data.load_all.assert_called_once()
        self.assertEqual(status_first, status_second)

    def test_get_by_const_fails_on_invalid_const(self):
        statuses = [{
            "id": 1,
            "const": "STATUS",
            "description": "Status Description"
        }]
        result = Result(True, "", statuses)
        result.set_affected_rows(len(statuses))
        self.status_data.load_all = MagicMock(return_value=result)

        with self.assertRaises(LicenseStatusFetchException):
            self.status_manager.get_by_const("WRONG_CONST")
            self.fail("Did not fail on missing status constant")

    def test_get_by_const_caches_on_second_call(self):
        statuses = [{
            "id": 1,
            "const": "STATUS",
            "description": "Status Description"
        }]
        result = Result(True, "", statuses)
        result.set_affected_rows(len(statuses))
        self.status_data.load_all = MagicMock(return_value=result)

        status_first = self.status_manager.get_by_const("STATUS")
        status_second = self.status_manager.get_by_const("STATUS")

        self.status_data.load_all.assert_called_once()
        self.assertEqual(status_first, status_second)
