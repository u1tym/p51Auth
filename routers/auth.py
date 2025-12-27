# -*- coding: utf-8 -*-
"""
認証関連のAPIエンドポイント
"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from models.auth_models import (
    PreRequestModel,
    PreRequestResponseModel,
    UnlockRequestModel,
    UnlockResponseModel
)
from services.auth_service import process_prerequest, process_unlock

# ルーターを作成
router = APIRouter(prefix="/portal/auth/api", tags=["認証"])


@router.post("/prerequest", response_model=PreRequestResponseModel)
async def prerequest(request: PreRequestModel) -> PreRequestResponseModel:
    """
    プレ要求エンドポイント
    
    マジックナンバーを取得する
    """
    try:
        success: bool
        detail: Optional[str]
        magic_number: int
        success, detail, magic_number = process_prerequest(request.USER)
        
        return PreRequestResponseModel(
            RESULT=success,
            DETAIL=detail,
            MAGIC_NUMBER=magic_number
        )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"サーバーエラーが発生しました: {str(e)}"
        )


@router.post("/unlock", response_model=UnlockResponseModel)
async def unlock(request: UnlockRequestModel) -> UnlockResponseModel:
    """
    開錠要求エンドポイント
    
    認証処理を実行する
    """
    try:
        success: bool
        detail: Optional[str]
        seq_number: int
        success, detail, seq_number = process_unlock(
            user=request.USER,
            magic_number=request.MAGIC_NUMBER,
            hash_pass=request.HASH_PASS
        )
        
        return UnlockResponseModel(
            RESULT=success,
            DETAIL=detail,
            SEQ_NUMBER=seq_number
        )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"サーバーエラーが発生しました: {str(e)}"
        )

