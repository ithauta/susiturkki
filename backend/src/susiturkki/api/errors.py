from fastapi import FastAPI
from fastapi.responses import JSONResponse

from susiturkki.domain.errors import RuleError

CLIENT_ERRORS = {
    "not_authenticated": 401,
    "invalid_credentials": 401,
    "group_not_found": 404,
    "participant_not_found": 404,
    "entry_not_found": 404,
    "group_not_empty": 409,
}


def register_errors(app: FastAPI) -> None:
    app.add_exception_handler(RuleError, _rule_error_response)


def _rule_error_response(_request, error: RuleError) -> JSONResponse:
    return JSONResponse({"code": error.code}, status_code=_status_for(error.code))


def _status_for(code: str) -> int:
    return CLIENT_ERRORS.get(code, 400)
