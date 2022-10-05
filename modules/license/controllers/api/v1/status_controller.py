from http import HTTPStatus
from flask import Blueprint
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.license.exceptions.license_status_fetch_exception import LicenseStatusFetchException
from modules.license.managers.status_manager import StatusManager
from service_locator import get_service_manager

license_status_v1_api = Blueprint("license_status_v1_api", __name__)
ROOT = "/v1/status"


@license_status_v1_api.route(f"{ROOT}", methods=["GET"])
def get_all_license_statuses():
    """ GET license statuses
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    status_manager: StatusManager = service_locator.get(StatusManager.__name__)
    try:
        statuses = status_manager.get_all()
        return HTTPResponse(HTTPStatus.OK, "", statuses).get_response()
    except LicenseStatusFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
