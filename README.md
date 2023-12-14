# README

### プロジェクト作成手順

Poetryでプロジェクトの初期設定をします。

```bash
$ poetry new api
Created package api in api
```

必要な開発ツールを導入します。

```bash
$ cd api
$ poetry add --group dev pytest pytest-cov black isort flake8
Creating virtualenv api in /workspace/api/.venv
```

pytestを実施するための仮想環境`.venv`も作成されます。

FastAPI, Mangumをインストールします。

```bash
$ poetry add fastapi uvicorn httpx
Using version ^0.105.0 for fastapi
Using version ^0.24.0.post1 for uvicorn
Using version ^0.25.2 for httpx
$ poetry add Mangum
Using version ^0.17.0 for mangum
```

main.pyを作成します

```python
#main.py

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


@app.get("/api-health-check/")
def health_check():
    return {"message": "OK"}


# Lambda Handler
lambda_handler = Mangum(app)
```

Terraformフォルダー作成
Terraform初期化
ECRを作成
```
# ecr.tf
resource "aws_ecr_repository" "fastapi_ecr" {
  name = "fastapi-lunch-blog-app-ecr"
}
```

AWSコンソールで作成したfastapi-lunch-blog-app-ecrリポジトリにアクセスし、プッシュコマンドを表示して、指示に従ってpush

Dockerfile作成
DockerImageBuild

