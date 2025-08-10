# CLAUDE.md

This file provides guidance to Claude Code when working with the Famoly Drive project.

## プロジェクト概要

**Famoly Drive** は家族でドライブ中に歴史を学べる教育アプリケーションです。

### 主な機能
- 🗺️ ルート検索（出発地→目的地）
- 📍 ルート周辺の歴史スポット自動検索
- 🎯 歴史スポットに関する教育クイズ
- 📊 スコア管理とランキング機能

## アーキテクチャ

### Frontend (Next.js 15)
- **フレームワーク**: Next.js 15 + TypeScript
- **スタイリング**: Tailwind CSS
- **地図**: Google Maps JavaScript API (現在はサンプルモード)
- **状態管理**: React hooks (useState)
- **通知**: react-hot-toast

### 主要コンポーネント
1. **app/page.tsx** - メイン画面（ルート情報、スコアボード、歴史スポット一覧）
2. **components/GoogleMapRoute.tsx** - Google Maps統合（本格運用時）
3. **components/SampleMapRoute.tsx** - サンプルデータでのデモ（現在使用中）
4. **components/WorkingQuizPanel.tsx** - 歴史クイズ機能

## 現在の開発状況

### 実装済み機能 ✅
- [x] Next.js基本構成とTailwind CSS設定
- [x] サンプルモードでのルート検索機能
- [x] 歴史スポット表示（鎌倉、京都、東京エリア対応）
- [x] 事前定義クイズシステム（スポット名ベース、難易度別）
- [x] スコア管理とランキング表示
- [x] Google Maps API統合準備完了

### 未実装機能 🚧
- [ ] OpenAI APIによる動的クイズ生成
- [ ] バックエンドAPIとの本格連携
- [ ] ユーザー認証とセッション管理
- [ ] データベースによる永続化
- [ ] より高度な歴史情報取得

### 現在のクイズシステム（事前定義版）
スポット名に基づく事前定義クイズを実装：
- **大仏** → 建立年代、制作者などの専門クイズ
- **八幡宮** → 源頼朝、鎌倉幕府関連クイズ  
- **神社** → 神道、地域信仰クイズ
- **寺・院** → 仏教、修行関連クイズ
- **城** → 戦国武将、軍事拠点クイズ
- **その他** → 一般的な歴史スポットクイズ

## 開発環境セットアップ

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

### Google Maps API統合（オプション）
1. Google Cloud Consoleでプロジェクト作成
2. 以下のAPIを有効化:
   - Maps JavaScript API
   - Places API
   - Directions API  
   - Geocoding API
3. `.env.local` に設定:
   ```
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key
   ```
4. `app/page.tsx` の `setIsGoogleMapsAvailable(true)` に変更

## サンプルデータ構成

### 対応ルート
- **東京駅 ⇄ 鎌倉駅**: 鎌倉大仏、鶴岡八幡宮、建長寺、円覚寺、銭洗弁財天
- **東京 ⇄ 京都**: 清水寺、金閣寺、伏見稲荷大社
- **その他**: 浅草寺、明治神宮、東京国立博物館

## 今後の拡張予定
- [ ] より多くの地域の歴史スポット追加
- [ ] ユーザー認証とデータベース連携
- [ ] クイズ問題のさらなる充実
- [ ] 音声ガイド機能
- [ ] 家族メンバー管理機能

## 重要な技術的詳細

### 状態管理
```typescript
const [currentRoute, setCurrentRoute] = useState<RouteInfo | null>(null)
const [historicalSpots, setHistoricalSpots] = useState<HistoricalSpot[]>([])
const [selectedSpot, setSelectedSpot] = useState<HistoricalSpot | null>(null)
const [userScore, setUserScore] = useState(0)
```

### クイズ生成関数
`WorkingQuizPanel.tsx` の `generateQuizForSpot()` 関数がスポット名を解析して適切なクイズタイプを選択

### 条件分岐レンダリング
Google Maps API利用可否に応じて `GoogleMapRoute` ↔ `SampleMapRoute` を自動切り替え

## トラブルシューティング

### Google Maps APIエラーの場合
- サンプルモードに切り替え: `setIsGoogleMapsAvailable(false)`
- API有効化手順を確認してからリアルモード使用

### 開発サーバー起動
```bash
cd frontend && npm run dev
```