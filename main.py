# -*- coding: utf-8 -*-
"""
FastAPI認証APIアプリケーション
制御部分（エントリーポイント）
"""

from fastapi import FastAPI
from routers import auth

# FastAPIアプリケーションを作成
app = FastAPI(
    title="認証API",
    description="認証処理を行うWeb API",
    version="1.0.0"
)

# ルーターを登録
app.include_router(auth.router)


@app.get("/")
async def root() -> dict[str, str]:
    """ルートエンドポイント"""
    return {"message": "認証APIサーバー"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
