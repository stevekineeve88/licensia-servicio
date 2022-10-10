import json
from http import HTTPStatus
from flask import Blueprint, request
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.license.exceptions.license_const_syntax_exception import LicenseConstSyntaxException
from modules.license.exceptions.license_create_exception import LicenseCreateException
from modules.license.exceptions.license_delete_exception import LicenseDeleteException
from modules.license.exceptions.license_fetch_exception import LicenseFetchException
from modules.license.exceptions.license_status_fetch_exception import LicenseStatusFetchException
from modules.license.exceptions.license_update_exception import LicenseUpdateException
from modules.license.managers.status_manager import StatusManager
from modules.license.managers.license_manager import LicenseManager
from service_locator import get_service_manager

license_v1_api = Blueprint("license_v1_api", __name__)
ROOT = "/v1/license"


@license_v1_api.route(f"{ROOT}", methods=["POST"])
def create_license():
    """ POST license
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    license_manager: LicenseManager = service_locator.get(LicenseManager.__name__)
    status_manager: StatusManager = service_locator.get(StatusManager.__name__)
    try:
        data = json.loads(request.get_data().decode())
        license_obj = license_manager.create(
            status_manager.get_by_const("ACTIVE"),
            data["const"],
            data["description"]
        )
        return HTTPResponse(HTTPStatus.CREATED, "", [license_obj]).get_response()
    except (LicenseCreateException, LicenseConstSyntaxException) as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@license_v1_api.route(f"{ROOT}/<license_id>", methods=["PATCH"])
def update_license_by_id(license_id: int):
    """ PATCH license information
    Args:
        license_id (int):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    license_manager: LicenseManager = service_locator.get(LicenseManager.__name__)
    try:
        license_obj = license_manager.get_by_id(int(license_id))

        data = json.loads(request.get_data().decode())
        license_obj.set_description(data["description"] if "description" in data else license_obj.get_description())

        new_license = license_manager.update(license_obj)
        return HTTPResponse(HTTPStatus.OK, "", [new_license]).get_response()
    except LicenseFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except LicenseUpdateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@license_v1_api.route(f"{ROOT}/<license_id>/status/<status_id>", methods=["PATCH"])
def update_license_status_by_license_id(license_id: int, status_id: int):
    """ PATCH license status
    Args:
        license_id (int):
        status_id (int):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    license_manager: LicenseManager = service_locator.get(LicenseManager.__name__)
    status_manager: StatusManager = service_locator.get(StatusManager.__name__)
    try:
        status = status_manager.get_by_id(int(status_id))
        license_obj = license_manager.update_status(int(license_id), status)
        return HTTPResponse(HTTPStatus.OK, "", [license_obj]).get_response()
    except LicenseUpdateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except (LicenseStatusFetchException, LicenseFetchException) as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@license_v1_api.route(f"{ROOT}/<license_id>", methods=["GET"])
def get_license_by_id(license_id: int):
    """ GET license
    Args:
        license_id (int):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    license_manager: LicenseManager = service_locator.get(LicenseManager.__name__)
    try:
        license_obj = license_manager.get_by_id(int(license_id))
        return HTTPResponse(HTTPStatus.OK, "", [license_obj]).get_response()
    except LicenseFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@license_v1_api.route(f"{ROOT}", methods=["GET"])
def search_licenses():
    """ GET licenses
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    license_manager: LicenseManager = service_locator.get(LicenseManager.__name__)
    try:
        query_params = request.args.to_dict()
        search_query = query_params.get("search") or ""
        limit = query_params.get("limit") or 10
        offset = query_params.get("offset") or 0

        result = license_manager.search(search=search_query, limit=int(limit), offset=int(offset))
        http_response = HTTPResponse(HTTPStatus.OK, "", result.get_licenses())
        http_response.set_meta({
            "total_count": result.get_total_count(),
            "search": search_query,
            "limit": limit,
            "offset": offset
        })
        return http_response.get_response()
    except LicenseFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@license_v1_api.route(f"{ROOT}/<license_id>", methods=["DELETE"])
def delete_license_by_id(license_id: int):
    """ DELETE license
    Args:
        license_id (int):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    license_manager: LicenseManager = service_locator.get(LicenseManager.__name__)
    try:
        license_manager.delete(int(license_id))
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except LicenseDeleteException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
