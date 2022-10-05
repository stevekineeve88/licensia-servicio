from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.license.data.factories.status_data_factory import StatusDataFactory
from modules.license.data.status_data import StatusData
from modules.license.managers.factories.status_manager_factory import StatusManagerFactory
from modules.license.managers.status_manager import StatusManager


class LicenseConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            StatusManager.__name__: StatusManagerFactory(),
            StatusData.__name__: StatusDataFactory()
        }
