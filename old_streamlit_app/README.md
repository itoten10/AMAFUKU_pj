# 旧Streamlitアプリケーション（アーカイブ）

このフォルダには、Famoly Driveの初期バージョン（Streamlit版）のファイルが保存されています。

## 含まれるファイル

- `app.py` - Streamlitメインアプリケーション
- `historical_data.py` - 歴史データ処理
- `historical_quiz.py` - クイズ生成ロジック
- `utils.py` - ユーティリティ関数
- `requirements.txt` - Streamlit版の依存関係
- `.env.streamlit` - Streamlit版の環境変数（Google Maps APIキー）
- `venv/` - Python仮想環境（Streamlit用）

## 現在のプロジェクト構成

現在のプロジェクトは以下の技術スタックに移行しています：

- **フロントエンド**: Next.js 15 + TypeScript（`/frontend`）
- **バックエンド**: FastAPI + OpenAI API（`/backend`）

## 注意

このフォルダのコードは参考用として保存されていますが、現在はメンテナンスされていません。
現在の開発は`/frontend`と`/backend`ディレクトリで行ってください。