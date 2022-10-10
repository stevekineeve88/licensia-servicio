from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.license.data.factories.license_data_factory import LicenseDataFactory
from modules.license.data.factories.status_data_factory import StatusDataFactory
from modules.license.data.license_data import LicenseData
from modules.license.data.status_data import StatusData
from modules.license.managers.factories.license_manager_factory import LicenseManagerFactory
from modules.license.managers.factories.status_manager_factory import StatusManagerFactory
from modules.license.managers.license_manager import LicenseManager
from modules.license.managers.status_manager import StatusManager


class LicenseConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            StatusManager.__name__: StatusManagerFactory(),
            StatusData.__name__: StatusDataFactory(),
            LicenseData.__name__: LicenseDataFactory(),
            LicenseManager.__name__: LicenseManagerFactory()
        }
