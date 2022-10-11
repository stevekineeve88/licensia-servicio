import time
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.license.exceptions.license_create_exception import LicenseCreateException
from modules.license.exceptions.license_delete_exception import LicenseDeleteException
from modules.license.exceptions.license_fetch_exception import LicenseFetchException
from modules.license.exceptions.license_update_exception import LicenseUpdateException
from modules.license.managers.license_manager import LicenseManager
from modules.license.managers.status_manager import StatusManager
from modules.license.objects.status import Status
from tests.integration.setup.integration_setup import IntegrationSetup


class LicenseManagerTest(IntegrationSetup):
    license_manager: LicenseManager = None
    connection_manager: ConnectionManager = None
    status_manager: StatusManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.license_manager = cls.service_locator.get(LicenseManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)

    def test_create_creates_license(self):
        status = self.status_manager.get_by_const("ACTIVE")
        expected_license = self.license_manager.create(status, "LICENSE", "Some Description")
        actual_license = self.license_manager.get_by_id(expected_license.get_id())

        self.assertEqual(expected_license.get_id(), actual_license.get_id())
        self.assertEqual(expected_license.get_uuid(), actual_license.get_uuid())
        self.assertEqual(expected_license.get_const(), actual_license.get_const())
        self.assertEqual(expected_license.get_description(), actual_license.get_description())
        self.assertEqual(status.get_id(), actual_license.get_status().get_id())
        self.assertEqual(expected_license.get_created_timestamp(), actual_license.get_created_timestamp())
        self.assertEqual(expected_license.get_update_timestamp(), actual_license.get_update_timestamp())

    def test_create_fails_on_duplicate_const(self):
        status = self.status_manager.get_by_const("ACTIVE")
        self.license_manager.create(status, "LICENSE", "Some Description")
        with self.assertRaises(LicenseCreateException):
            self.license_manager.create(status, "LICENSE", "Some Description 2")
            self.fail("Did not fail on create for duplicate license constant")

    def test_create_fails_on_invalid_status(self):
        with self.assertRaises(LicenseCreateException):
            self.license_manager.create(Status(123456, "INVALID_STATUS", "Description"), "LICENSE", "Some Description")
            self.fail("Did not fail on create for invalid status")

    def test_get_by_id_fails_on_invalid_id(self):
        with self.assertRaises(LicenseFetchException):
            self.license_manager.get_by_id(1)
            self.fail("Did not fail on fetch by invalid ID")

    def test_update_updates_license(self):
        license_obj = self.license_manager.create(self.status_manager.get_by_const("ACTIVE"), "CONST", "Description")
        time.sleep(3)

        new_description = "new description"
        license_obj.set_description(new_description)
        new_license_obj = self.license_manager.update(license_obj)

        self.assertEqual(license_obj.get_description(), new_license_obj.get_description())
        self.assertNotEqual(license_obj.get_update_timestamp(), new_license_obj.get_update_timestamp())

    def test_update_status_updates_status(self):
        old_status = self.status_manager.get_by_const("ACTIVE")
        new_status = self.status_manager.get_by_const("INACTIVE")

        license_obj = self.license_manager.create(
            old_status,
            "CONST",
            "Description"
        )

        self.license_manager.update_status(license_obj.get_uuid(), new_status)
        new_license_obj = self.license_manager.get_by_id(license_obj.get_id())

        self.assertEqual(new_status.get_id(), new_license_obj.get_status().get_id())

    def test_update_status_fails_on_invalid_status_id(self):
        license_obj = self.license_manager.create(
            self.status_manager.get_by_const("ACTIVE"),
            "CONST",
            "Description"
        )
        with self.assertRaises(LicenseUpdateException):
            self.license_manager.update_status(license_obj.get_uuid(), Status(123456, "SOME_CONST", "Description"))
            self.fail("Did not fail on update status for invalid status ID")

    def test_delete_deletes_license(self):
        license_obj = self.license_manager.create(
            self.status_manager.get_by_const("ACTIVE"),
            "CONST",
            "Description"
        )
        self.license_manager.delete(license_obj.get_uuid())

        with self.assertRaises(LicenseFetchException):
            self.license_manager.get_by_id(license_obj.get_id())
            self.fail("Did not fail on missing deleted license")

    def test_delete_fails_on_invalid_id(self):
        with self.assertRaises(LicenseDeleteException):
            self.license_manager.delete("sfsdfsdf")
            self.fail("Did not fail on delete for invalid ID")

    def test_search_searches_licenses(self):
        active_status = self.status_manager.get_by_const("ACTIVE")

        self.license_manager.create(
            active_status,
            "CONST",
            "Description"
        )
        self.license_manager.create(
            active_status,
            "CONST_ONE",
            "Description 1"
        )
        self.license_manager.create(
            active_status,
            "CONST_TWO",
            "Description 2"
        )

        license_result = self.license_manager.search(search="one")

        self.assertEqual(1, len(license_result.get_licenses()))
        self.assertEqual(1, license_result.get_total_count())

    def test_search_paginates(self):
        active_status = self.status_manager.get_by_const("ACTIVE")
        self.license_manager.create(
            active_status,
            "CONST",
            "Description"
        )
        self.license_manager.create(
            active_status,
            "CONST_ONE",
            "Description 1"
        )
        self.license_manager.create(
            active_status,
            "CONST_TWO",
            "Description 2"
        )

        lic_result_1 = self.license_manager.search(search="const", limit=1, offset=0)
        lic_result_2 = self.license_manager.search(search="const", limit=1, offset=1)

        self.assertEqual(1, len(lic_result_1.get_licenses()))
        self.assertEqual(1, len(lic_result_2.get_licenses()))

        self.assertEqual(3, lic_result_1.get_total_count())
        self.assertEqual(3, lic_result_2.get_total_count())

        self.assertEqual("CONST", lic_result_1.get_licenses()[0].get_const())
        self.assertEqual("CONST_ONE", lic_result_2.get_licenses()[0].get_const())

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM license WHERE 1=1
        """)
        if not result.get_status():
            raise Exception(f"Failed to teardown license test instance: {result.get_message()}")
