# 🤝 Claude Code チーム開発ガイド

## ⚠️ 最重要ルール

### 1. 作業開始時の必須手順
```bash
git pull origin main
# 必ずCLAUDE.mdを最初に読む
# 変更があれば相方と確認
git checkout -b feature/your-feature-name
```

### 2. Claude Code特有の注意点

#### **CLAUDE.mdは神聖不可侵**
- すべての開発情報の中枢
- 変更時は必ず相方に通知
- Claudeは最初にこのファイルを読む

#### **コミットメッセージ統一**
```bash
git commit -m "機能: 具体的な変更

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## 🚨 避けるべき状況

### 同時編集禁止ファイル
- `CLAUDE.md` - 事前調整必須
- `package.json` / `requirements.txt` - 依存関係競合
- 環境設定ファイル

### デバッグ情報の共有
```bash
# エラー発生時の共有形式
git commit -m "WIP: [問題] 具体的なエラー内容

再現手順:
1. 
2. 
3. 

エラーメッセージ:
```
[具体的なエラー]
```

相方へ: 詳細はissue #XX参照

🤖 Generated with [Claude Code](https://claude.ai/code)"
```

## 💡 効率的な開発フロー

### Issue活用
```markdown
# GitHub Issue テンプレート
## 概要
- 何を実装/修正するか

## 技術詳細
- 使用技術・ライブラリ
- 影響するファイル

## Claude Codeへの指示
- 実装方針
- 注意事項
```

### プルリクエスト
```markdown
# PR説明テンプレート
## 変更内容
- 

## CLAUDE.md更新
- [ ] 機能追加を反映
- [ ] セットアップ手順更新

## 動作確認
- [ ] ローカルでテスト完了
- [ ] 依存関係確認済み

## Claude Codeメモ
相方への引き継ぎ事項:
- 
```

## 🔧 環境同期チェックリスト

### 初回セットアップ
- [ ] Node.js version確認 (package.jsonのengines参照)
- [ ] Python version確認
- [ ] .env設定完了
- [ ] 依存関係インストール
- [ ] 動作確認完了

### 定期確認
- [ ] CLAUDE.mdの最新内容確認
- [ ] package.json / requirements.txt差分確認
- [ ] API key等の環境変数更新

## 🎯 開発分担提案

### Phase 1: 基盤強化
- **Person A**: 認証システム、ユーザー管理
- **Person B**: データベース設計、API拡張

### Phase 2: 機能拡張
- **Person A**: UI/UX改善、レスポンシブ対応
- **Person B**: 地図機能強化、パフォーマンス最適化

### Phase 3: 高度機能
- **Person A**: 音声ガイド、オフライン対応
- **Person B**: AI機能拡張、分析機能

## 📞 緊急時の対応

### ビルドエラー時
1. エラーログをそのままissueに貼り付け
2. 最後に成功したcommit hashを記載
3. 環境情報（OS、Node version等）も添付

### API制限に達した時
1. `.env.example`のモデル設定変更
2. フォールバック機能の動作確認
3. 使用量を共有して調整

---
**このファイルは定期的に更新し、問題・改善点があれば随時追記してください。**