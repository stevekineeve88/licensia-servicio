from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.license.data.status_data import StatusData
from modules.license.managers.status_manager import StatusManager


class StatusManagerFactory(FactoryInterface):
    """ Factory for creating status manager objects
    """
    def invoke(self, service_manager):
        return StatusManager(
            status_data=service_manager.get(StatusData.__name__)
        )
