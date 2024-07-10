from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
import uvicorn

from api.router import router

app = FastAPI()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
