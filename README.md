# 認証API

FastAPIを使用した認証Web APIアプリケーション

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

