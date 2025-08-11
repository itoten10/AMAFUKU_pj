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
2. **components/EnhancedGoogleMapRoute.tsx** - 教育強化版Google Maps（地理的分散ロジック搭載）
3. **components/EnhancedSampleMapRoute.tsx** - 教育強化版サンプルモード（地理的分散対応）
4. **components/GoogleMapRoute.tsx** - 標準Google Maps統合
5. **components/SampleMapRoute.tsx** - 標準サンプルモード
6. **components/WorkingQuizPanel.tsx** - 基本クイズ機能
7. **components/AIQuizPanel.tsx** - OpenAI統合AIクイズ生成

## 現在の開発状況

### 実装済み機能 ✅
- [x] Next.js基本構成とTailwind CSS設定
- [x] サンプルモードでのルート検索機能
- [x] 歴史スポット表示（鎌倉、京都、東京エリア対応）
- [x] 事前定義クイズシステム（スポット名ベース、難易度別）
- [x] スコア管理とランキング表示
- [x] Google Maps API統合準備完了
- [x] **OpenAI APIによる動的クイズ生成（gpt-3.5-turbo使用）**
- [x] **教育強化版ルート検索（日本史・地理特化）**
- [x] **地理的分散ロジック（10区間分割による均等スポット配置）**
- [x] **FastAPI + OpenAI統合バックエンド（simple_api.py）**
- [x] **教育価値評価システム（国宝・史跡優先度付け）**

### 未実装機能 🚧
- [ ] ユーザー認証とセッション管理
- [ ] データベースによる永続化
- [ ] より高度な歴史情報取得
- [ ] 音声ガイド機能

### クイズシステム（2種類対応）

#### 1. AIクイズシステム（OpenAI統合）✨
- **OpenAI API**: gpt-3.5-turbo使用（コスト効率重視）
- **動的生成**: スポット名・説明から自動でクイズ作成
- **難易度調整**: 小学生・中学生・高校生レベル対応
- **コスト**: 約0.1円/クイズ（約300トークン使用）
- **フォールバック**: API障害時は事前定義クイズに自動切り替え

#### 2. 事前定義クイズシステム（基本版）
スポット名に基づく事前定義クイズを実装：
- **大仏** → 建立年代、制作者などの専門クイズ
- **八幡宮** → 源頼朝、鎌倉幕府関連クイズ  
- **神社** → 神道、地域信仰クイズ
- **寺・院** → 仏教、修行関連クイズ
- **城** → 戦国武将、軍事拠点クイズ
- **その他** → 一般的な歴史スポットクイズ

## 地理的分散ロジック（新機能）🎯

### 課題解決
- **課題**: スポットが地理的に固まってしまう問題
- **解決**: ルートを10区間に分割して各区間から1スポットずつ抽出

### アルゴリズム
1. **ルート分割**: Google Maps経路を10等分
2. **区間別検索**: 各区間8km圏内で歴史スポット検索
3. **教育価値評価**: 国宝・重要文化財 > 史跡 > 城郭・神社・寺院
4. **重複排除**: 同一スポットの除去
5. **距離制限**: 最小1km間隔での分散配置

### 教育価値スコアリング
```
国宝・重要文化財・世界遺産: +100点
史跡・特別史跡: +80点  
古戦場・合戦場: +75点
城郭・天守: +70点
神社・寺院: +60点
古墳・遺跡: +65点
```

## 開発環境セットアップ

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

### Backend（OpenAI統合）
```bash
cd backend
pip install -r simple_requirements.txt

# 環境変数設定
cp .env.example .env
# .envにOPENAI_API_KEYを設定

# サーバー起動
uvicorn simple_api:app --reload --port 8000
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

## ファイル構成

### Frontend（Next.js）
```
frontend/
├── app/
│   ├── page.tsx                           # メインページ
│   └── layout.tsx
├── components/
│   ├── EnhancedGoogleMapRoute.tsx         # 教育強化版Google Maps
│   ├── EnhancedSampleMapRoute.tsx         # 教育強化版サンプルモード
│   ├── GoogleMapRoute.tsx                 # 標準Google Maps
│   ├── SampleMapRoute.tsx                 # 標準サンプルモード
│   ├── AIQuizPanel.tsx                    # OpenAI統合クイズ
│   └── WorkingQuizPanel.tsx               # 基本クイズ
└── package.json
```

### Backend（FastAPI + OpenAI）
```
backend/
├── simple_api.py                          # OpenAI統合API
├── simple_requirements.txt                # 最小依存関係
├── .env.example                           # 環境変数テンプレート
└── app/                                   # 旧バックエンド（参考用）
```

## トラブルシューティング

### Google Maps APIエラーの場合
- サンプルモードに切り替え: `setIsGoogleMapsAvailable(false)`
- API有効化手順を確認してからリアルモード使用

### OpenAI APIエラーの場合
- `.env`ファイルに`OPENAI_API_KEY`が正しく設定されているか確認
- API利用制限・クレジット残高を確認
- フォールバック機能により基本クイズが自動提供される

### 開発サーバー起動
```bash
# フロントエンド
cd frontend && npm run dev

# バックエンド（AIクイズ機能用）
cd backend && uvicorn simple_api:app --reload --port 8000
```