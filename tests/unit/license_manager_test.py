import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result

from modules.license.data.license_data import LicenseData
from modules.license.exceptions.license_const_syntax_exception import LicenseConstSyntaxException
from modules.license.managers.license_manager import LicenseManager
from modules.license.managers.status_manager import StatusManager
from modules.license.objects.status import Status


class UserManagerTest(unittest.TestCase):

    @patch("modules.license.data.license_data.LicenseData")
    @patch("modules.license.managers.status_manager.StatusManager")
    def setUp(
            self,
            license_data: LicenseData,
            status_manager: StatusManager
    ) -> None:
        self.license_data = license_data
        self.status_manager = status_manager
        self.license_manager: LicenseManager = LicenseManager(
            license_data=self.license_data,
            status_manager=self.status_manager
        )

    def test_create_fails_on_invalid_symbol(self):
        self.license_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(LicenseConstSyntaxException):
            self.license_manager.create(Status(1, "CONST", "description"), "LICENSE_$#%DF", "Description")
            self.fail("Did not fail on invalid symbols in const for creating license")
        self.license_data.insert.assert_not_called()

    def test_create_fails_on_lowercase_letters(self):
        self.license_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(LicenseConstSyntaxException):
            self.license_manager.create(Status(1, "CONST", "description"), "LiCENSE", "Description")
            self.fail("Did not fail on lower case letters in const for creating license")
        self.license_data.insert.assert_not_called()

    def test_search_defaults_limit_if_over_100(self):
        self.license_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 101,
            "offset": 0
        }

        self.license_manager.search(**params)
        self.license_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_limit_if_under_0(self):
        self.license_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": -1,
            "offset": 0
        }

        self.license_manager.search(**params)
        self.license_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_offset_if_under_0(self):
        self.license_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 20,
            "offset": -1
        }

        self.license_manager.search(**params)
        self.license_data.search.assert_called_once_with(
            search=params["search"],
            limit=params["limit"],
            offset=0
        )
