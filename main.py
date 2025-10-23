import time
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

app = FastAPI(title="Simple FastAPI Boilerplate")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Request to {request.url} processed in {process_time:.4f} seconds")
    return response

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello, World!"}

@app.get("/health", tags=["Monitoring"])
async def health_check():
    return JSONResponse(content={"status": "healthy"}, status_code=200)


@app.get("/items/{item_id}", tags=["Items"])
async def read_item(item_id: int):
    return {"item_id": item_id, "item_name": "Example Item"}

@app.post("/items/", tags=["Items"])
async def create_item(name: str):
    return {"message": f"Item '{name}' created successfully"}