# -*- coding: utf-8 -*-
"""
FastAPI認証APIアプリケーション
"""

from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import sys
import os

# comlibsをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'comlibs'))

from authorize import Authorize
from config import auth_config

app = FastAPI(
    title="認証API",
    description="認証処理を行うWeb API",
    version="1.0.0"
)


# リクエストモデル
class PreRequestModel(BaseModel):
    """プレ要求リクエストモデル"""
    USER: str = Field(..., description="試行ユーザ名")


class UnlockRequestModel(BaseModel):
    """開錠要求リクエストモデル"""
    USER: str = Field(..., description="試行ユーザ名")
    MAGIC_NUMBER: int = Field(..., description="マジックナンバ")
    HASH_PASS: str = Field(..., description="ハッシュ化パスワード")


# レスポンスモデル
class PreRequestResponseModel(BaseModel):
    """プレ要求レスポンスモデル"""
    RESULT: bool = Field(..., description="結果(True/False)")
    DETAIL: Optional[str] = Field(None, description="結果がFalseだった場合に詳細情報を設定")
    MAGIC_NUMBER: int = Field(..., description="マジックナンバ")


class UnlockResponseModel(BaseModel):
    """開錠要求レスポンスモデル"""
    RESULT: bool = Field(..., description="結果(True/False)")
    DETAIL: Optional[str] = Field(None, description="結果がFalseだった場合に詳細情報を設定")
    SEQ_NUMBER: int = Field(..., description="シーケンス管理ナンバ")


def get_error_detail(result_code: int) -> str:
    """エラーコードから詳細メッセージを取得"""
    error_messages: dict[int, str] = {
        -1: "該当ユーザが存在しない",
        -2: "認証不正",
        -9: "処理異常"
    }
    return error_messages.get(result_code, "不明なエラー")


@app.post("/portal/auth/api/prerequest", response_model=PreRequestResponseModel)
async def prerequest(request: PreRequestModel) -> PreRequestResponseModel:
    """
    プレ要求エンドポイント
    
    マジックナンバーを取得する
    """
    try:
        # Authorizeインスタンスを生成
        authorize = Authorize(
            dbhost=auth_config.dbhost,
            dbport=auth_config.dbport,
            dbname=auth_config.dbname,
            dbuser=auth_config.dbuser,
            dbpass=auth_config.dbpass
        )
        
        # get_magic_number()を呼び出す
        magic_number: int = authorize.get_magic_number(user=request.USER)
        
        # 戻り値が0以上のときは正常、負数のときは異常
        if magic_number >= 0:
            return PreRequestResponseModel(
                RESULT=True,
                DETAIL=None,
                MAGIC_NUMBER=magic_number
            )
        else:
            return PreRequestResponseModel(
                RESULT=False,
                DETAIL=get_error_detail(magic_number),
                MAGIC_NUMBER=magic_number
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"サーバーエラーが発生しました: {str(e)}"
        )


@app.post("/portal/auth/api/unlock", response_model=UnlockResponseModel)
async def unlock(request: UnlockRequestModel) -> UnlockResponseModel:
    """
    開錠要求エンドポイント
    
    認証処理を実行する
    """
    try:
        # Authorizeインスタンスを生成
        authorize = Authorize(
            dbhost=auth_config.dbhost,
            dbport=auth_config.dbport,
            dbname=auth_config.dbname,
            dbuser=auth_config.dbuser,
            dbpass=auth_config.dbpass
        )
        
        # try_unlock()を呼び出す
        seq_number: int = authorize.try_unlock(
            user=request.USER,
            magic=request.MAGIC_NUMBER,
            pass_hash=request.HASH_PASS
        )
        
        # 戻り値が0以上のときは正常、負数のときは異常
        if seq_number >= 0:
            return UnlockResponseModel(
                RESULT=True,
                DETAIL=None,
                SEQ_NUMBER=seq_number
            )
        else:
            return UnlockResponseModel(
                RESULT=False,
                DETAIL=get_error_detail(seq_number),
                SEQ_NUMBER=seq_number
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"サーバーエラーが発生しました: {str(e)}"
        )


@app.get("/")
async def root() -> dict[str, str]:
    """ルートエンドポイント"""
    return {"message": "認証APIサーバー"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

