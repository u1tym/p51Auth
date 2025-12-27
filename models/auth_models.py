# -*- coding: utf-8 -*-
"""
認証関連のリクエスト/レスポンスモデル
"""

from typing import Optional
from pydantic import BaseModel, Field


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

