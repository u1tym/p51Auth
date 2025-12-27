# -*- coding: utf-8 -*-
"""
認証関連の業務ロジック
"""

import sys
import os
from typing import Tuple, Optional

# comlibsをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'comlibs'))

from authorize import Authorize
from config import auth_config


def get_error_detail(result_code: int) -> str:
    """
    エラーコードから詳細メッセージを取得
    
    Args:
        result_code: エラーコード
    
    Returns:
        エラーメッセージ
    """
    error_messages: dict[int, str] = {
        -1: "該当ユーザが存在しない",
        -2: "認証不正",
        -9: "処理異常"
    }
    return error_messages.get(result_code, "不明なエラー")


def create_authorize_instance() -> Authorize:
    """
    Authorizeインスタンスを生成
    
    Returns:
        Authorizeインスタンス
    """
    return Authorize(
        dbhost=auth_config.dbhost,
        dbport=auth_config.dbport,
        dbname=auth_config.dbname,
        dbuser=auth_config.dbuser,
        dbpass=auth_config.dbpass
    )


def process_prerequest(user: str) -> Tuple[bool, Optional[str], int]:
    """
    プレ要求の業務ロジック処理
    
    Args:
        user: ユーザー名
    
    Returns:
        (成功フラグ, エラー詳細, マジックナンバー)のタプル
    """
    authorize: Authorize = create_authorize_instance()
    magic_number: int = authorize.get_magic_number(user=user)
    
    if magic_number >= 0:
        return (True, None, magic_number)
    else:
        return (False, get_error_detail(magic_number), magic_number)


def process_unlock(user: str, magic_number: int, hash_pass: str) -> Tuple[bool, Optional[str], int]:
    """
    開錠要求の業務ロジック処理
    
    Args:
        user: ユーザー名
        magic_number: マジックナンバー
        hash_pass: ハッシュパス
    
    Returns:
        (成功フラグ, エラー詳細, シーケンス番号)のタプル
    """
    authorize: Authorize = create_authorize_instance()
    seq_number: int = authorize.try_unlock(
        user=user,
        magic=magic_number,
        pass_hash=hash_pass
    )
    
    if seq_number >= 0:
        return (True, None, seq_number)
    else:
        return (False, get_error_detail(seq_number), seq_number)

