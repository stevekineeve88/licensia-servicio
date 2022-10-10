from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.license.data.license_data import LicenseData


class LicenseDataFactory(FactoryInterface):
    """ Factory for creating license data object
    """
    def invoke(self, service_manager):
        return LicenseData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
