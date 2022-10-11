from typing import Dict, List
from modules.license.data.license_data import LicenseData
from modules.license.exceptions.license_const_syntax_exception import LicenseConstSyntaxException
from modules.license.exceptions.license_create_exception import LicenseCreateException
from modules.license.exceptions.license_delete_exception import LicenseDeleteException
from modules.license.exceptions.license_fetch_exception import LicenseFetchException
from modules.license.exceptions.license_update_exception import LicenseUpdateException
from modules.license.managers.status_manager import StatusManager
from modules.license.objects.license import License
from modules.license.objects.license_search_result import LicenseSearchResult
from modules.license.objects.status import Status


class LicenseManager:
    """ Manager for license objects
    """
    def __init__(self, **kwargs):
        """ Constructor for LicenseManager
        Args:
            **kwargs:           Dependencies
                license_data (LicenseData)              - License data layer
                status_manager (StatusManager)          - Status object manager
        """
        self.__license_data: LicenseData = kwargs.get("license_data")
        self.__status_manager: StatusManager = kwargs.get("status_manager")

    def create(self, status: Status, const: str, description: str) -> License:
        """ Create license
        Args:
            status (Status):
            const (str):
            description (str):
        Returns:
            License
        """
        self.__check_const(const)
        result = self.__license_data.insert(status.get_id(), const=const, description=description)
        if not result.get_status():
            raise LicenseCreateException(f"Could not create license: {result.get_message()}")
        return self.get_by_id(result.get_last_insert_id())

    def get_by_id(self, license_id: int) -> License:
        """ Get by ID
        Args:
            license_id (int):           License ID
        Returns:
            License
        """
        result = self.__license_data.load_by_id(license_id)
        if result.get_affected_rows() == 0:
            raise LicenseFetchException(f"Could not fetch license with ID {license_id} ")
        return self.__build_license_obj(result.get_data()[0])

    def get_by_uuid(self, license_uuid: str) -> License:
        """ Get by UUID
        Args:
            license_uuid (str):
        Returns:
            License
        """
        result = self.__license_data.load_by_uuid(license_uuid)
        if result.get_affected_rows() == 0:
            raise LicenseFetchException(f"Could not fetch license with UUID {license_uuid}")
        return self.__build_license_obj(result.get_data()[0])

    def update(self, license_obj: License) -> License:
        """ Update license
        Args:
            license_obj (License):
        Returns:
            License
        """
        result = self.__license_data.update(license_obj.get_id(), description=license_obj.get_description())
        if not result.get_status():
            raise LicenseUpdateException(f"Could not update license with ID {license_obj.get_id()}")
        return self.get_by_id(license_obj.get_id())

    def update_status(self, license_uuid: str, status: Status) -> License:
        """ Update license status
        Args:
            license_uuid (str):
            status (Status):
        Returns:
            License
        """
        result = self.__license_data.update_status(license_uuid, status.get_id())
        if not result.get_status():
            raise LicenseUpdateException(f"Could not update status for license with UUID {license_uuid}")
        return self.get_by_uuid(license_uuid)

    def delete(self, license_uuid: str):
        """ Delete license
        Args:
            license_uuid (str):
        """
        result = self.__license_data.delete(license_uuid)
        if result.get_affected_rows() == 0:
            raise LicenseDeleteException(f"Could not delete license with UUID {license_uuid}")

    def search(self, **kwargs) -> LicenseSearchResult:
        """ Search licenses
        Args:
            **kwargs:           Search params
                search (str)
                limit (int)
                offset (int)
        Returns:
            LicenseSearchResult
        """
        limit = kwargs.get("limit") or 100
        limit = limit if 100 >= limit > 0 else 10

        offset = kwargs.get("offset") or 0
        offset = offset if offset >= 0 else 0

        search = kwargs.get("search") or ""

        result = self.__license_data.search(
            search=search,
            limit=limit,
            offset=offset
        )
        if not result.get_status():
            raise LicenseFetchException(f"Could not search licences: {result.get_message()}")

        data = result.get_data()
        licenses: List[License] = []
        for datum in data:
            licenses.append(self.__build_license_obj(datum))

        result = self.__license_data.search_count(search)
        if not result.get_status():
            raise LicenseFetchException(f"Could not fetch license count: {result.get_message()}")

        return LicenseSearchResult(licenses, result.get_data()[0]["count"])

    @classmethod
    def __check_const(cls, const: str):
        """ Check license constant for standard
        Args:
            const (str):        Constant to check
        """
        pieces = const.split("_")
        for piece in pieces:
            if not piece.isalpha() or piece.upper() != piece:
                raise LicenseConstSyntaxException(
                    "Constant definition must be capital snake case"
                )

    def __build_license_obj(self, data: Dict[str, any]) -> License:
        """ Build license object
        Args:
            data: (Dict[str, any])
        Returns:
            License
        """
        return License(
            self.__status_manager.get_by_id(data["status_id"]),
            id=data["id"],
            uuid=data["uuid"],
            const=data["const"],
            description=data["description"],
            created_timestamp=data["created_timestamp"],
            update_timestamp=data["update_timestamp"]
        )
