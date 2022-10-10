from typing import List
from modules.license.objects.license import License


class LicenseSearchResult:
    """ Object representing license search result
    """
    def __init__(self, licenses: List[License], total_count):
        """ Constructor for LicenseSearchResult
        Args:
            licenses (List[License]):   License list of search
            total_count (int):          Total un-paginated count
        """
        self.__licenses: List[License] = licenses
        self.__total_count: int = total_count

    def get_licenses(self) -> List[License]:
        """ Get licenses
        Returns:
            List[License]
        """
        return self.__licenses

    def get_total_count(self) -> int:
        """ Get total count
        Returns:
            int
        """
        return self.__total_count
