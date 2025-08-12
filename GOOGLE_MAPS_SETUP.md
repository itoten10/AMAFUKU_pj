# Google Maps API セットアップガイド

## 現在の設定

APIキー: `AIzaSyBRmDlXpXGPfyVtzmXX6-8dP2_vDCvTJKA`
設定場所: `frontend/.env.local`

## Google Cloud Consoleでの設定確認

### 1. 必要なAPIの有効化

以下のAPIが有効になっているか確認してください：

1. **Maps JavaScript API** - 地図表示用
2. **Places API** - 場所検索用
3. **Directions API** - ルート検索用
4. **Geocoding API** - 住所変換用

### 有効化手順：
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを選択
3. 「APIとサービス」→「ライブラリ」
4. 上記の各APIを検索して「有効にする」をクリック

### 2. APIキーの制限設定

セキュリティのため、APIキーに適切な制限を設定します：

1. 「APIとサービス」→「認証情報」
2. 該当のAPIキーをクリック
3. 「アプリケーションの制限」で以下を設定：

#### 開発環境の場合：
- **HTTPリファラー（ウェブサイト）**を選択
- 以下のURLを追加：
  ```
  http://localhost:3000/*
  http://localhost:3001/*
  http://127.0.0.1:3000/*
  ```

#### 本番環境の場合：
- 実際のドメインを追加（例：`https://yourdomain.com/*`）

### 3. API制限の設定
「APIの制限」セクションで、使用するAPIのみを選択：
- Maps JavaScript API
- Places API
- Directions API
- Geocoding API

## トラブルシューティング

### エラー: "The Google Maps JavaScript API could not load"

**原因と対処法：**

1. **APIが有効化されていない**
   - 上記の4つのAPIすべてが有効か確認

2. **APIキーの制限が厳しすぎる**
   - 開発中は一時的に「制限なし」にして動作確認
   - 動作確認後、適切な制限を設定

3. **請求先アカウントが設定されていない**
   - Google Cloud Consoleで請求先アカウントを設定
   - 無料枠：月$200相当まで無料

4. **APIキーが間違っている**
   - `frontend/.env.local`のキーを確認
   - Google Cloud Consoleで正しいキーをコピー

### エラー: "RefererNotAllowedMapError"

HTTPリファラーの制限に現在のURLが含まれていません。
上記の「APIキーの制限設定」を確認してください。

### エラー: "InvalidKeyMapError"

APIキーが無効です。以下を確認：
- APIキーが正しくコピーされているか
- APIキーが有効になっているか
- プロジェクトが正しいか

## 動作確認方法

1. フロントエンドを起動：
   ```bash
   cd frontend
   npm run dev
   ```

2. http://localhost:3000 にアクセス

3. ブラウザの開発者ツール（F12）でコンソールを確認

4. エラーが表示されていなければ成功

## 無料枠について

Google Maps Platform は月$200相当まで無料で使用できます：
- Maps JavaScript API: 28,000回/月まで無料
- Places API: 5,000回/月まで無料
- Directions API: 5,000回/月まで無料

通常の開発・テストでは無料枠を超えることはありません。

## サポート

問題が解決しない場合は、以下の情報と共に報告してください：
- ブラウザのコンソールエラー全文
- Google Cloud Consoleの設定スクリーンショット
- 実行環境（OS、ブラウザ等）