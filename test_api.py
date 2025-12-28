# -*- coding: utf-8 -*-
"""
APIテストスクリプト
仕様2.txtに基づくテストケースを実行

使用方法:
  1. 環境変数で指定:
     export API_HOST=example.com
     export API_PORT=9000
     python test_api.py
  
  2. コマンドライン引数で指定:
     python test_api.py --host example.com --port 9000
  
  3. デフォルト値: localhost:8000
"""

import os
import zlib
import argparse
import requests
from typing import Dict, Any, Optional

# APIのベースURL（main()で設定される）
BASE_URL: str = "http://localhost:8000"


def calculate_hash_pass(upass: str, magic: int) -> str:
    """
    ハッシュパスを算出
    
    Args:
        upass: パスワード
        magic: マジックナンバー
    
    Returns:
        ハッシュパス（8桁の16進数文字列）
    """
    combined: str = f"{upass}{magic}"
    hash_pass: str = format(zlib.crc32(combined.encode()) & 0xFFFFFFFF, '08x')
    return hash_pass


def print_test_header(test_number: int, description: str) -> None:
    """テストヘッダーを表示"""
    print("\n" + "=" * 80)
    print(f"テスト {test_number}: {description}")
    print("=" * 80)


def print_request(url: str, method: str, data: Dict[str, Any]) -> None:
    """リクエスト内容を表示"""
    print(f"\n[送信内容]")
    print(f"  URL: {url}")
    print(f"  メソッド: {method}")
    print(f"  データ: {data}")


def print_response(response: requests.Response) -> None:
    """レスポンス内容を表示"""
    print(f"\n[受信内容]")
    print(f"  ステータスコード: {response.status_code}")
    try:
        json_data: Dict[str, Any] = response.json()
        print(f"  レスポンス: {json_data}")
        return json_data
    except Exception as e:
        print(f"  レスポンス解析エラー: {e}")
        print(f"  生レスポンス: {response.text}")
        return {}


def print_result(expected_success: bool, actual_result: bool, test_passed: bool) -> None:
    """テスト結果を表示"""
    print(f"\n[テスト結果]")
    print(f"  期待値: {'正常' if expected_success else '異常'}")
    print(f"  実際の結果: {'正常' if actual_result else '異常'}")
    print(f"  判定: {'✓ PASS' if test_passed else '✗ FAIL'}")


def test_prerequest(user: str, expected_success: bool) -> Optional[int]:
    """
    プレ要求のテスト
    
    Args:
        user: ユーザー名
        expected_success: 正常が返ることを期待するか
    
    Returns:
        成功した場合のMAGIC_NUMBER、失敗した場合はNone
    """
    url: str = f"{BASE_URL}/portal/auth/api/prerequest"
    data: Dict[str, str] = {"USER": user}
    
    print_request(url, "POST", data)
    
    try:
        response: requests.Response = requests.post(url, json=data)
        json_data: Dict[str, Any] = print_response(response)
        
        actual_result: bool = json_data.get("RESULT", False)
        test_passed: bool = (actual_result == expected_success)
        
        print_result(expected_success, actual_result, test_passed)
        
        if actual_result:
            magic_number: int = json_data.get("MAGIC_NUMBER", 0)
            return magic_number
        else:
            detail: Optional[str] = json_data.get("DETAIL")
            if detail:
                print(f"  エラー詳細: {detail}")
            return None
            
    except Exception as e:
        print(f"\n[エラー] リクエスト送信エラー: {e}")
        print_result(expected_success, False, False)
        return None


def test_unlock(user: str, magic_number: int, hash_pass: str, expected_success: bool) -> Optional[int]:
    """
    開錠要求のテスト
    
    Args:
        user: ユーザー名
        magic_number: マジックナンバー
        hash_pass: ハッシュパス
        expected_success: 正常が返ることを期待するか
    
    Returns:
        成功した場合のSEQ_NUMBER、失敗した場合はNone
    """
    url: str = f"{BASE_URL}/portal/auth/api/unlock"
    data: Dict[str, Any] = {
        "USER": user,
        "MAGIC_NUMBER": magic_number,
        "HASH_PASS": hash_pass
    }
    
    print_request(url, "POST", data)
    
    try:
        response: requests.Response = requests.post(url, json=data)
        json_data: Dict[str, Any] = print_response(response)
        
        actual_result: bool = json_data.get("RESULT", False)
        test_passed: bool = (actual_result == expected_success)
        
        print_result(expected_success, actual_result, test_passed)
        
        if actual_result:
            seq_number: int = json_data.get("SEQ_NUMBER", 0)
            return seq_number
        else:
            detail: Optional[str] = json_data.get("DETAIL")
            if detail:
                print(f"  エラー詳細: {detail}")
            return None
            
    except Exception as e:
        print(f"\n[エラー] リクエスト送信エラー: {e}")
        print_result(expected_success, False, False)
        return None


def get_base_url() -> str:
    """
    環境変数またはコマンドライン引数からベースURLを取得
    
    Returns:
        ベースURL（例: http://localhost:8000）
    """
    # 環境変数からデフォルト値を取得
    default_host: str = os.getenv("API_HOST", "localhost")
    default_port_str: str = os.getenv("API_PORT", "8000")
    try:
        default_port: int = int(default_port_str)
    except ValueError:
        default_port = 8000
    
    parser = argparse.ArgumentParser(
        description="APIテストスクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--host",
        type=str,
        default=default_host,
        help="APIサーバーのホスト名（デフォルト: localhost または環境変数 API_HOST）"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=default_port,
        help="APIサーバーのポート番号（デフォルト: 8000 または環境変数 API_PORT）"
    )
    
    args = parser.parse_args()
    base_url: str = f"http://{args.host}:{args.port}"
    return base_url


def main() -> None:
    """メイン処理"""
    global BASE_URL
    BASE_URL = get_base_url()
    
    print("=" * 80)
    print("APIテスト開始")
    print(f"接続先: {BASE_URL}")
    print("=" * 80)
    
    # テスト1: プレ要求（USER = admin）
    print_test_header(1, "プレ要求（USER = admin）")
    magic_admin: Optional[int] = test_prerequest("admin", expected_success=True)
    
    # テスト2: プレ要求（USER = sample）
    print_test_header(2, "プレ要求（USER = sample）")
    magic_sample: Optional[int] = test_prerequest("sample", expected_success=True)
    
    # テスト3: プレ要求（USER = xxxx）
    print_test_header(3, "プレ要求（USER = xxxx）")
    test_prerequest("xxxx", expected_success=False)
    
    # テスト4: 開錠要求（USER = admin）
    print_test_header(4, "開錠要求（USER = admin）")
    if magic_admin is not None:
        password_admin: str = "admin"
        hash_pass_admin: str = calculate_hash_pass(password_admin, magic_admin)
        print(f"\n[準備] パスワード='{password_admin}', MAGIC_NUMBER={magic_admin}")
        print(f"  算出したHASH_PASS: {hash_pass_admin}")
        test_unlock("admin", magic_admin, hash_pass_admin, expected_success=True)
    else:
        print("\n[スキップ] テスト1でMAGIC_NUMBERが取得できなかったため、テスト4をスキップします")
    
    # テスト5: 開錠要求（USER = sample）
    print_test_header(5, "開錠要求（USER = sample）")
    if magic_sample is not None:
        password_sample: str = "sample"
        hash_pass_sample: str = calculate_hash_pass(password_sample, magic_sample)
        print(f"\n[準備] パスワード='{password_sample}', MAGIC_NUMBER={magic_sample}")
        print(f"  算出したHASH_PASS: {hash_pass_sample}")
        test_unlock("sample", magic_sample, hash_pass_sample, expected_success=True)
    else:
        print("\n[スキップ] テスト2でMAGIC_NUMBERが取得できなかったため、テスト5をスキップします")
    
    # テスト6: 開錠要求（不正な値）
    print_test_header(6, "開錠要求（不正な値）")
    test_unlock("sample", 0, "xxxx", expected_success=False)
    
    print("\n" + "=" * 80)
    print("APIテスト終了")
    print("=" * 80)


if __name__ == "__main__":
    main()

