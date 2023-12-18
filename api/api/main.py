from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from routers import post
from utils.logger import logger

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# エラーハンドリング
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """リクエストのバリデーションエラーをハンドリングする
    RequestValidationErrorが発生する時、400 Bad Requestを返す
    """
    logger.error(f"RequestValidationError: {exc}")
    return JSONResponse(status_code=400, content={"message": "Bad Request."})


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """ルーターで発生したHTTPExceptionをハンドリングする"""
    logger.error(f"HTTPException: {exc}")
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


# GET /health-check APIのためのルーティング
@app.get("/health-check")
def health_check():
    return {"message": "OK"}


app.router.include_router(post.router)


# Lambda Handler
lambda_handler = Mangum(app)
