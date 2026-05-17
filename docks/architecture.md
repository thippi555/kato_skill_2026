# Architecture

## 1. 概要

本ツールは、スキルシートおよびGitHubリポジトリ情報をもとに、職務経験・技術領域・担当工程・役割をAIで分析し、面接向けに可視化するツールである。

初期構成では、AIエージェントによる自律実行ではなく、定義済みの固定ワークフローとして構成する。

---

## 2. 目的

本ツールの目的は以下である。

- スキルシートの内容を構造化する
- GitHub上の成果物を分析対象に含める
- 職務経験を技術領域ごとに可視化する
- 面接で説明しやすい実績サマリを生成する
- 将来的なAIエージェント化に備えた構成とする

---

## 3. 初期アーキテクチャ

```text
User / Web UI
      ↓
API Gateway
      ↓
Step Functions
      ↓
Lambda
  ├─ GitHub API取得
  ├─ スキルシート解析
  ├─ Bedrock呼び出し
  ├─ 分析結果整形
  └─ S3 / DynamoDB保存
      ↓
Dashboard / Streamlit

## 4. 利用サービス

| 領域 | サービス | 用途 |
|---|---|---|
| API受付 | Amazon API Gateway | 分析処理の起動 |
| ワークフロー | AWS Step Functions | 処理順序、分岐、リトライ制御 |
| 処理実行 | AWS Lambda | GitHub取得、解析、Bedrock呼び出し |
| AI分析 | Amazon Bedrock | 職務経験・技術領域の分析 |
| 入力管理 | GitHub API | README、コード、コミット情報の取得 |
| 保存 | Amazon S3 | 入力ファイル、分析結果JSONの保存 |
| メタデータ保存 | Amazon DynamoDB | 分析履歴、ステータス、結果参照先の管理 |
| 可視化 | Streamlit / Web UI | グラフ、一覧、面接用サマリの表示 |

---

# 5. 処理フロー

## 5.1 分析開始

ユーザーはWeb UIまたはAPI経由で、分析対象のGitHubリポジトリURLやスキルシート情報を指定する。

---

## 5.2 ワークフロー起動

API GatewayからStep Functionsを起動し、分析処理を開始する。

---

## 5.3 GitHub情報取得

LambdaでGitHub APIを呼び出し、以下の情報を取得する。

- README
- リポジトリ構成
- 主要ソースコード
- 使用言語
- コミット履歴
- docs配下の設計資料

---

## 5.4 スキル情報抽出

取得した情報から、以下の要素を抽出する。

- 技術スタック
- 担当工程
- 役割
- 成果物
- クラウドサービス
- AI活用箇所
- 開発・運用プロセス

---

## 5.5 AI分析

Amazon Bedrockを呼び出し、抽出情報をもとに職務経験を構造化する。

出力はJSON形式とし、後続の可視化処理で利用しやすい形式に統一する。

---

## 5.6 結果保存

分析結果をS3にJSONとして保存し、DynamoDBに分析履歴と参照先を保存する。

---

## 5.7 可視化

StreamlitまたはWeb UIで、以下を表示する。

- 技術領域別の経験マップ
- 工程別の経験割合
- クラウドサービス利用状況
- 案件タイムライン
- 面接で説明すべき実績
- 想定質問と回答例

---

# 6. AgentCoreを初期構成で利用しない理由

初期構成ではAmazon Bedrock AgentCoreを利用しない。

理由は以下である。

- 処理フローが固定されている
- AIに自律的なTool選択を任せない
- GitHub取得、分析、保存、可視化の流れが明確である
- Step Functionsで処理順序とリトライを制御できる
- 最小構成で実装・検証しやすい

AgentCoreは、AIエージェントが自律的にToolを選択し、複数の外部システムを操作する段階で利用を検討する。

---

# 7. Step Functionsを利用する理由

Step Functionsを利用する理由は以下である。

- 処理の流れを明示的に管理できる
- GitHub取得、AI分析、保存処理を分離できる
- エラー時のリトライを定義できる
- 処理状態を可視化できる
- 将来的に分岐や並列処理を追加しやすい

本ツールでは、AIに処理順序を任せるのではなく、業務フローとして明確に制御する。

---

# 8. MCPを初期構成で利用しない理由

初期構成ではMCPを利用しない。

理由は以下である。

- 呼び出す外部ツールが限定的である
- GitHub APIとBedrock呼び出しで主要機能を実現できる
- Tool連携を標準化する段階ではない
- まずは固定ワークフローの完成を優先する

MCPは、将来的に以下を統合する段階で検討する。

- GitHub
- Jira
- Backlog
- Notion
- Google Drive
- AWS / Azure / GCP見積API
- 社内ナレッジベース

---

# 9. データ構造方針

AI分析結果はJSON形式で保存する。

想定するJSON構造は以下である。

```json
{
  "profile_summary": "クラウド、AI、データ基盤、業務システム開発に強みを持つエンジニア",
  "skill_categories": [
    {
      "category": "Cloud",
      "skills": ["AWS", "GCP", "Azure"],
      "experience_level": "High"
    },
    {
      "category": "AI",
      "skills": ["Bedrock", "LLM", "RAG"],
      "experience_level": "Medium"
    }
  ],
  "projects": [
    {
      "name": "AI進捗管理システム",
      "role": "設計・開発",
      "technologies": ["AWS", "Lambda", "Bedrock", "S3"],
      "summary": "成果物をAIで評価し、進捗率や品質スコアを可視化する仕組み"
    }
  ],
  "interview_points": [
    "AIを活用した業務効率化の経験",
    "クラウド上でのサーバレス設計経験",
    "設計から実装まで一貫して対応できる点"
  ]
}

# 10. セキュリティ方針

初期構成では以下を考慮する。

- GitHub TokenはSecrets Managerまたは環境変数で管理する
- API Gatewayには認証を設定する
- LambdaのIAM権限は最小権限とする
- S3バケットは非公開とする
- 分析対象に個人情報が含まれる可能性を考慮する
- Bedrockへ送信するデータは必要最小限にする

---

# 11. 将来拡張

将来的には以下を検討する。

- AgentCoreによる自律分析エージェント化
- MCPによる外部ツール連携の標準化
- GitHub Actionsとの連携
- 面接質問の自動生成
- 職種別の自己PR生成
- スキルギャップ分析
- 学習計画生成
- 求人票とのマッチング分析
- ReactベースのWeb UI化
- TerraformによるAWS環境構築

---

# 12. 構成判断まとめ

| 判断項目 | 初期方針 |
|---|---|
| 実行方式 | 固定ワークフロー |
| ワークフロー制御 | Step Functions |
| AI実行 | Bedrock |
| 自律エージェント | 初期は利用しない |
| AgentCore | 将来拡張 |
| MCP | 将来拡張 |
| 可視化 | Streamlit |
| 保存 | S3 / DynamoDB |
| IaC | 将来的にTerraform対応 |

---

# 13. 現時点の結論

初期構成では、AgentCoreやMCPを利用せず、API Gateway、Step Functions、Lambda、Bedrockを中心とした固定ワークフロー型の構成とする。

これにより、最小構成で実装しやすく、かつ将来的なAIエージェント化にも拡張しやすい構成とする。