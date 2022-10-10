from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.license.data.license_data import LicenseData
from modules.license.managers.license_manager import LicenseManager
from modules.license.managers.status_manager import StatusManager


class LicenseManagerFactory(FactoryInterface):
    """ Factory for creating license manager object
    """
    def invoke(self, service_manager):
        return LicenseManager(
            license_data=service_manager.get(LicenseData.__name__),
            status_manager=service_manager.get(StatusManager.__name__)
        )
