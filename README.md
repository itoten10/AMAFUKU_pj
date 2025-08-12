# Famoly Drive - AMAFUKU Project

移動時間を学習時間に変える、新しい家族体験

## プロジェクト構成

```
AMAFUKU_PJ/
├── frontend/          # Next.js 15 フロントエンド
├── backend/           # FastAPI バックエンド  
├── old_streamlit_app/ # 旧Streamlitアプリ（アーカイブ）
├── CLAUDE.md          # Claude Code開発ガイド
├── ENV_SETUP_GUIDE.md # 環境変数設定ガイド
└── TEAM_DEVELOPMENT.md # チーム開発ガイドライン
```

## クイックスタート

### バックエンド
```bash
cd backend
cp .env.example .env  # APIキーを設定
pip install -r simple_requirements.txt
uvicorn simple_api:app --reload --port 8000
```

### フロントエンド
```bash
cd frontend
npm install
npm run dev
```

詳細は[CLAUDE.md](./CLAUDE.md)を参照してください。