from datetime import datetime
from typing import Dict
from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict
from modules.license.objects.status import Status


class License(HTTPDict):
    """ Object representing license
    """
    def __init__(self, status: Status, **kwargs):
        """ Constructor for License
        Args:
            status (Status):        License status object
            **kwargs:               License info
                id (int)
                uuid (str)
                const (str)
                description (str)
                created_timestamp (datetime)
                update_timestamp (datetime)
        """
        self.__id: int = kwargs.get("id")
        self.__uuid: str = kwargs.get("uuid")
        self.__const: str = kwargs.get("const")
        self.__description: str = kwargs.get("description")
        self.__status: Status = status
        self.__created_timestamp: datetime = kwargs.get("created_timestamp")
        self.__update_timestamp: datetime = kwargs.get("update_timestamp")

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.__id

    def get_uuid(self) -> str:
        """ Get UUID
        Returns:
            str
        """
        return self.__uuid

    def get_const(self) -> str:
        """ Get constant
        Returns:
            str
        """
        return self.__const

    def get_description(self) -> str:
        """ Get description
        Returns:
            str
        """
        return self.__description

    def set_description(self, description: str):
        """ Set description
        Args:
            description (str):
        """
        self.__description = description

    def get_status(self) -> Status:
        """ Get status
        Returns:
            Status
        """
        return self.__status

    def get_created_timestamp(self) -> datetime:
        """ Get created timestamp
        Returns:
            datetime
        """
        return self.__created_timestamp

    def get_update_timestamp(self) -> datetime:
        """ Get update timestamp
        Returns:
            datetime
        """
        return self.__update_timestamp

    def get_http_dict(self) -> Dict[str, any]:
        """ Get HTTP dict of object
        Returns:
            Dict [str, any]
        """
        date_format = "%Y-%m-%d %H:%M:%S"
        status = self.get_status()
        return {
            "id": self.get_id(),
            "uuid": self.get_uuid(),
            "const": self.get_const(),
            "description": self.get_description(),
            "status": {
                "id": status.get_id(),
                "const": status.get_const(),
                "description": status.get_description()
            },
            "created_timestamp": self.get_created_timestamp().strftime(date_format),
            "update_timestamp": self.get_update_timestamp().strftime(date_format)
        }
