# Famoly Drive - 移動時間を学習時間に

家族でドライブしながら楽しく学習できるWebアプリケーション

## 機能

- **ルート検索**: Google Maps APIを使用した出発地から目的地までのルート検索
- **歴史スポット表示**: ルート周辺の歴史的な場所を自動検出
- **クイズ機能**: 各スポットに関する難易度別クイズ（小学生/中学生/高校生）
- **スコア管理**: ユーザーごとのポイント管理とランキング表示
- **リアルタイム地図**: インタラクティブな地図表示とスポット情報

## 技術スタック

### バックエンド
- FastAPI (Python)
- SQLAlchemy + SQLite/PostgreSQL
- Google Maps API
- JWT認証

### フロントエンド  
- Next.js 15 (React 19)
- TypeScript
- Tailwind CSS
- Leaflet (地図表示)
- Zustand (状態管理)
- React Query (データフェッチ)

## セットアップ

### 必要な環境
- Python 3.10+
- Node.js 18+
- Google Maps API Key

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd AMAFUKU_PJ
```

### 2. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .envファイルを編集してGoogle Maps APIキーを設定

# データベースの初期化（自動）
# サーバー起動
uvicorn main:app --reload --port 8000
```

### 3. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 環境変数の設定
# .env.localファイルを編集
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# 開発サーバー起動
npm run dev
```

### 4. アプリケーションへのアクセス

- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs

## 使い方

1. **新規登録/ログイン**
   - 初回利用時は新規登録画面でアカウントを作成
   - ユーザー名、メールアドレス、パスワードを入力

2. **ルート検索**
   - 出発地と目的地を入力（例: 東京駅、鎌倉駅）
   - 「ルート検索」ボタンをクリック

3. **歴史スポットの確認**
   - 地図上にオレンジ色のマーカーで歴史スポットが表示
   - マーカーをクリックして詳細情報を表示

4. **クイズに挑戦**
   - スポットの詳細から「クイズに挑戦」をクリック
   - 難易度を選択してクイズを生成
   - 正解するとポイントを獲得

5. **ランキング確認**
   - 右サイドバーでリアルタイムのランキングを確認
   - 自分のスコアと順位を確認

## プロジェクト構造

```
AMAFUKU_PJ/
├── backend/                # FastAPIバックエンド
│   ├── app/
│   │   ├── api/           # APIエンドポイント
│   │   ├── core/          # 設定・セキュリティ
│   │   ├── db/            # データベース設定
│   │   ├── models/        # SQLAlchemyモデル
│   │   ├── schemas/       # Pydanticスキーマ
│   │   └── services/      # ビジネスロジック
│   ├── main.py            # アプリケーションエントリーポイント
│   └── requirements.txt   # Python依存関係
│
├── frontend/              # Next.jsフロントエンド
│   ├── app/              # Next.js App Router
│   ├── components/       # Reactコンポーネント
│   ├── lib/              # ユーティリティ
│   ├── store/            # 状態管理
│   ├── types/            # TypeScript型定義
│   └── package.json      # Node.js依存関係
│
└── README_NEW.md         # このファイル
```

## API エンドポイント

### 認証
- `POST /api/v1/auth/register` - 新規登録
- `POST /api/v1/auth/login` - ログイン

### ユーザー
- `GET /api/v1/users/me` - 現在のユーザー情報
- `PUT /api/v1/users/me` - ユーザー情報更新
- `GET /api/v1/users/ranking` - ランキング取得

### ルート
- `POST /api/v1/routes/search` - ルート検索
- `POST /api/v1/routes/save` - ルート保存
- `GET /api/v1/routes/history` - 検索履歴

### クイズ
- `POST /api/v1/quizzes/generate` - クイズ生成
- `POST /api/v1/quizzes/attempt` - 回答送信
- `GET /api/v1/quizzes/history` - クイズ履歴

## トラブルシューティング

### Google Maps APIキーエラー
- Google Cloud Consoleで以下のAPIを有効化:
  - Maps JavaScript API
  - Places API
  - Geocoding API
  - Directions API

### CORS エラー
- バックエンドの`app/core/config.py`でCORS設定を確認
- フロントエンドのAPIベースURLが正しいか確認

### データベース接続エラー
- SQLiteの場合: 自動作成されるため問題ないはず
- PostgreSQLの場合: DATABASE_URLを正しく設定

## ライセンス

MIT License