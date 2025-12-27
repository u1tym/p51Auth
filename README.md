# 認証API

FastAPIを使用した認証Web APIアプリケーション

## ファイル構成

```
p51Auth/
├── main.py                    # 制御部分（FastAPIアプリの初期化とルーター登録）
├── config.py                  # 環境変数設定モジュール
├── test_api.py                # APIテストスクリプト
├── requirements.txt            # 依存パッケージ一覧
├── env.template               # 環境変数テンプレート
├── routers/                   # APIエンドポイント（ルーティング）
│   ├── __init__.py
│   └── auth.py               # 認証関連のAPIエンドポイント
├── services/                  # 業務ロジック
│   ├── __init__.py
│   └── auth_service.py       # 認証関連の業務ロジック
├── models/                    # リクエスト/レスポンスモデル
│   ├── __init__.py
│   └── auth_models.py         # 認証関連のモデル
├── comlibs/                   # 共通ライブラリ
│   ├── authorize.py          # Authorizeクラス
│   └── requirements.txt
└── document/                  # ドキュメント
    ├── 仕様1.txt
    └── 仕様2.txt
```

### 各ディレクトリ・ファイルの役割

#### ルートディレクトリ

- **`main.py`**: FastAPIアプリケーションのエントリーポイント。アプリの初期化とルーターの登録を行う制御部分。
- **`config.py`**: `.env`ファイルから環境変数を読み込み、設定を管理するモジュール。
- **`test_api.py`**: APIの動作をテストするスクリプト。
- **`requirements.txt`**: プロジェクトで使用するPythonパッケージの一覧。
- **`env.template`**: 環境変数のテンプレートファイル。

#### `routers/` ディレクトリ

APIエンドポイント（ルーティング）を定義するディレクトリ。HTTPリクエストの受付、サービス層の呼び出し、レスポンスの返却を担当。

- **`auth.py`**: 認証関連のAPIエンドポイント（`/portal/auth/api/prerequest`, `/portal/auth/api/unlock`）

#### `services/` ディレクトリ

業務ロジックを実装するディレクトリ。データベースアクセスやビジネスロジックを担当。

- **`auth_service.py`**: 認証関連の業務ロジック（プレ要求処理、開錠要求処理）

#### `models/` ディレクトリ

リクエスト/レスポンスのデータモデルを定義するディレクトリ。Pydanticモデルを使用。

- **`auth_models.py`**: 認証関連のリクエスト/レスポンスモデル

#### `comlibs/` ディレクトリ

共通ライブラリを配置するディレクトリ。

- **`authorize.py`**: 認証処理を行う`Authorize`クラス

### 新しいAPIを追加する方法

1. **モデルの追加**: `models/`ディレクトリに新しいモデルファイルを作成（例：`models/user_models.py`）
2. **サービスの追加**: `services/`ディレクトリに業務ロジックを追加（例：`services/user_service.py`）
3. **ルーターの追加**: `routers/`ディレクトリに新しいルーターファイルを作成（例：`routers/user.py`）
4. **ルーターの登録**: `main.py`に`app.include_router(user.router)`を追加

この構成により、各APIを独立したファイルとして管理でき、保守性と拡張性が向上します。

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`env.template`ファイルをコピーして`.env`ファイルを作成し、データベース接続情報を設定してください：

```bash
# Windows (PowerShell)
Copy-Item env.template .env

# Linux/Mac
cp env.template .env
```

`.env`ファイルを編集して、実際のデータベース接続情報を設定：

```env
Auth_dbhost=localhost
Auth_dbport=5432
Auth_dbname=your_database
Auth_dbuser=your_user
Auth_dbpass=your_password
```

### 3. サーバーの起動

```bash
python main.py
```

または

```bash
uvicorn main:app --reload
```

## API エンドポイント

- **プレ要求**: `POST /portal/auth/api/prerequest`
- **開錠要求**: `POST /portal/auth/api/unlock`

APIドキュメント: `http://localhost:8000/docs`

