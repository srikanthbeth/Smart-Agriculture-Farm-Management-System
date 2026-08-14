from fastapi import (
    Request,
    status
)

from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError


def register_exception_handlers(app):

    @app.exception_handler(
        IntegrityError
    )
    async def integrity_error_handler(
        request: Request,
        exc: IntegrityError
    ):

        return JSONResponse(
            status_code=400,
            content={
                "error": "Database integrity error",
                "detail": (
                    "The requested operation "
                    "violates a database constraint."
                )
            }
        )

    @app.exception_handler(
        ValueError
    )
    async def value_error_handler(
        request: Request,
        exc: ValueError
    ):

        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid value",
                "detail": str(exc)
            }
        )