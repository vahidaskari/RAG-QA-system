from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.endpoints import rag_endpoints
from app.config.settings import settings
from app.exceptions import GeneralException

app = FastAPI(title=settings.APP_NAME)


@app.exception_handler(GeneralException)
async def unicorn_exception_handler(request: Request, exc: GeneralException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


app.include_router(rag_endpoints.router, prefix="", tags=[settings.APP_NAME])
