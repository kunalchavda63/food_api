from fastapi import FastAPI, Request
import time

async def request_logger_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = (time.time() - start) * 1000
    print(f"{request.method} {request.url.path} completed_in={process_time:.2f}ms status={response.status_code}")
    return response