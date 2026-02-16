from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException


class ValidationErrorDetail(BaseModel):
    loc: tuple[str | int, ...] = Field(..., description="Location of the error in the request")
    msg: str = Field(..., description="A human-readable message for the error")
    type: str = Field(..., description="The type of the error")


class ErrorResponse(BaseModel):
    code: str = Field(..., description="A unique, machine-readable error code")
    message: str = Field(..., description="A human-readable message for the error")
    details: list[ValidationErrorDetail] | None = Field(
        None, description="Optional details for validation errors"
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler for FastAPI's built-in HTTPException.

    This handler formats the error into a standard ErrorResponse model.
    It supports passing a dictionary with 'code' and 'message' in exc.detail.
    """
    if isinstance(exc.detail, dict):
        # If detail is a dict, assume it matches our convention
        code = exc.detail.get("code", "http_exception")
        message = exc.detail.get("message", "An unexpected error occurred.")
    else:
        # If detail is a string, wrap it in the standard format
        code = "http_exception"
        message = str(exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ErrorResponse(code=code, message=message)),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for Pydantic's RequestValidationError."""
    details = [
        ValidationErrorDetail(loc=err["loc"], msg=err["msg"], type=err["type"])
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            ErrorResponse(
                code="validation_error", message="Input validation failed", details=details
            )
        ),
    )