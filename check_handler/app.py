from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from starlette import status


class CustomException(Exception):
    pass


async def some_dep():
    print("inside dep")
    try:
        yield 123
    except Exception as e:
        print("exception occurred")  # it disappears with custom handler
    finally:
        print("finally in dep")


def create_app() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        print("startup action")

    @app.on_event("shutdown")
    async def shutdown():
        print("shutdown action")

    # when commenting line below "exception occurred" line appears on post request
    install_exception_handlers(app)

    @app.post("/qwe")
    async def qwe(a: int = Depends(some_dep)):
        print(a)
        raise CustomException

    return app


def install_exception_handlers(app: FastAPI):
    @app.exception_handler(CustomException)
    async def postgres_error_handler(_: Request, __: CustomException) -> JSONResponse:
        return JSONResponse(
            dict(response="this is json response"),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
