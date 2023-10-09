from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# 引入你的路由模組
from app.api import api_user
from app.auth import authentication

app = FastAPI()

origins = [
    "http://0.0.0.0:8080",  # 前端地址
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.get("/")
def read_root():
    return {"Hello": "World"}

# import 分支router
app.include_router(authentication.router)
app.include_router(api_user.router)

@app.exception_handler(HTTPException)  # HTTP異常類型
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )

@app.exception_handler(Exception)  # 通用異常類型
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500, 
        content={"message": "An unexpected error occurred: " + str(exc)}
    )