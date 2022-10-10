from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class LicenseData:
    """ Data layer for license database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for LicenseData
        Args:
            **kwargs:           Dependencies
                connection_manager (ConnectionManager)          - Connection manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, status_id: int, **kwargs) -> Result:
        """ Insert license
        Args:
            status_id (int):        Status ID
            **kwargs:               License information
                const (str)
                description (str)
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO license (const, description, status_id)
            VALUES (%(const)s, %(description)s, %(status_id)s)
        """, {
            "const": kwargs.get("const"),
            "description": kwargs.get("description"),
            "status_id": status_id,
        })

    def load_by_id(self, license_id: int) -> Result:
        """ Load by ID
        Args:
            license_id (int):      License ID
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                license.id,
                bin_to_uuid(license.uuid) as uuid,
                license.const,
                license.description,
                license.status_id,
                license.created_timestamp,
                license.update_timestamp
            FROM license
            WHERE license.id = %(id)s
        """, {
            "id": license_id
        })

    def update(self, license_id: int, **kwargs) -> Result:
        """ Update license information
        Args:
            license_id (int):          License ID
            **kwargs:                  License information to update
                description (str)
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            UPDATE license SET description = %(description)s
            WHERE id = %(id)s
        """, {
            "description": kwargs.get("description"),
            "id": license_id
        })

    def update_status(self, license_id: int, status_id: int) -> Result:
        """ Update license status
        Args:
            license_id (int):   License ID
            status_id (int):    Status ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            UPDATE license SET status_id = %(status_id)s
            WHERE id = %(id)s
        """, {
            "status_id": status_id,
            "id": license_id
        })

    def delete(self, license_id: int) -> Result:
        """ Delete license
        Args:
            license_id (int):      License ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM license WHERE id = %(id)s
        """, {
            "id": license_id
        })

    def search(self, **kwargs) -> Result:
        """ Search licenses
        Args:
            **kwargs:           Search params
                search (str)
                limit (int)
                offset (int)
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                license.id,
                bin_to_uuid(license.uuid) as uuid,
                license.const,
                license.description,
                license.status_id,
                license.created_timestamp,
                license.update_timestamp
            FROM license
            {self.__build_search_query()}
            ORDER BY license.const ASC
            LIMIT %(limit)s OFFSET %(offset)s
        """, {
            "search": f"%{kwargs.get('search')}%",
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset")
        })

    def search_count(self, search) -> Result:
        """ Get count of search
        Args:
            search (str):
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                COUNT(*) AS count
            FROM license
            {self.__build_search_query()}
        """, {
            "search": f"%{search}%"
        })

    @classmethod
    def __build_search_query(cls) -> str:
        """ Build search query for licenses
        Returns:
            str
        """
        return f"""
            WHERE license.const LIKE %(search)s
                OR license.description LIKE %(search)s
        """
