# 🔧 環境変数セットアップガイド

## 必要なAPIキー

### 1. OpenAI API
- **目的**: AIクイズ生成機能
- **取得方法**: https://platform.openai.com/api-keys
- **コスト**: gpt-3.5-turbo使用で約0.1円/クイズ
- **必須度**: ⭐⭐⭐ (AIクイズ機能に必須)

### 2. Google Maps API (オプション)
- **目的**: リアルタイム地図・ルート検索
- **取得方法**: https://console.cloud.google.com/
- **有効化API**:
  - Maps JavaScript API
  - Places API
  - Directions API
  - Geocoding API
- **必須度**: ⭐ (サンプルモードで代替可能)

### 3. その他の設定
- **SECRET_KEY**: JWT トークン用（ランダム文字列）
- **DATABASE_URL**: SQLite使用（変更不要）

## セットアップ手順

```bash
# 1. テンプレートをコピー
cp backend/.env.example backend/.env

# 2. APIキーを設定
# .envファイルを編集して実際のキーに置き換え

# 3. 動作確認
cd backend && uvicorn simple_api:app --reload --port 8000
```

## APIキー取得ガイド

### OpenAI API Key 取得
1. https://platform.openai.com/ にアクセス
2. アカウント作成・ログイン
3. API Keys > Create new secret key
4. キーをコピー（一度しか表示されない）
5. 料金設定で上限を設定推奨

### Google Maps API Key 取得
1. Google Cloud Console にアクセス
2. 新しいプロジェクト作成
3. 必要なAPIを有効化
4. 認証情報 > APIキー作成
5. キーの制限設定（セキュリティ向上）

## 💰 コスト管理

### OpenAI API
- **現在の設定**: gpt-3.5-turbo (最安)
- **トークン制限**: 300トークン/リクエスト
- **推定コスト**: $0.001/クイズ (約0.15円)

### Google Maps API
- **月間無料枠**: $200相当
- **Maps JavaScript API**: $7/1000回
- **Places API**: $17/1000回

## 🔒 セキュリティ注意事項

⚠️ **絶対にしてはいけないこと**
- APIキーをGitHubにコミット
- 公開チャットに投稿
- メールで平文送信

✅ **推奨する共有方法**
- OneTimeSecret (https://onetimesecret.com/)
- 暗号化ファイル + 別ルートでパスワード共有
- Signal等の暗号化メッセージ

## トラブルシューティング

### OpenAI APIエラー
```
401 Unauthorized → APIキーが間違っている
429 Rate limit → 使用量制限に達した
```

### Google Maps APIエラー
```
ApiNotActivatedMapError → APIが有効化されていない
RefererNotAllowedMapError → ドメイン制限の設定確認
```

---
**このガイドは機密情報を含まないため、GitHubに安全にコミットできます。**