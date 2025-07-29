import logging
import time
import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from src.clients.fastapi.routers import tasks
from starlette.exceptions import HTTPException as StarletteHTTPException


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("fastapi")


app = FastAPI(title="tasks_base")
app.include_router(tasks.router)
app.include_router(tasks.land_page)
app.include_router(tasks.health_check)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Completed in {process_time:.2f}s: {request.method} {request.url.path} → {response.status_code}")
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": F"Bad request, request:{request.url}, Error: {exc.detail}"})


if __name__ == '__main__':
    uvicorn.run("tasks_base:app", reload=True)
