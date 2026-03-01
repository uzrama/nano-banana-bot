from fastapi import HTTPException
from starlette import status


class HTTPError(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal Server Error"

    def __init__(self, msg: str | None = None) -> None:
        super().__init__(status_code=self.status_code, detail=msg or self.detail)
