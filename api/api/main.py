from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GET /health-check APIのためのルーティング
@app.get("/health-check")
def health_check():
    return {"message": "OK"}


# Lambda Handler
lambda_handler = Mangum(app)
