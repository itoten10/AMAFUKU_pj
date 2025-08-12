from typing import Dict, List, Optional
import logging
from openai import AsyncOpenAI
from ..core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        ) if settings.OPENAI_API_KEY else None
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE

    async def generate_quiz(
        self, 
        spot_name: str, 
        spot_description: str, 
        difficulty: str = "中学生"
    ) -> Optional[Dict]:
        """
        歴史スポット情報からクイズを動的生成
        コスト効率を重視した実装
        """
        if not self.client:
            logger.warning("OpenAI API key not configured")
            return None

        try:
            # 難易度に応じたポイント設定
            points = {"小学生": 10, "中学生": 15, "高校生": 20}.get(difficulty, 15)
            
            # コスト効率重視のプロンプト（短く、明確に）
            prompt = self._build_prompt(spot_name, spot_description, difficulty)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            quiz_text = response.choices[0].message.content
            parsed_quiz = self._parse_quiz_response(quiz_text, points)
            
            # コスト追跡のためのログ
            logger.info(f"Quiz generated for {spot_name} - Tokens used: {response.usage.total_tokens}")
            
            return parsed_quiz

        except Exception as e:
            logger.error(f"OpenAI quiz generation error: {e}")
            return None

    def _build_prompt(self, spot_name: str, spot_description: str, difficulty: str) -> str:
        """コスト効率重視の短いプロンプト"""
        return f"""
{spot_name}について{difficulty}レベルのクイズを1問作成してください。

スポット情報: {spot_description}

以下の形式で回答:
問題: [4択問題文]
1. [選択肢1]
2. [選択肢2]  
3. [選択肢3]
4. [選択肢4]
正解: [1-4の数字]
解説: [簡潔な解説文]
""".strip()

    def _parse_quiz_response(self, response: str, points: int) -> Dict:
        """OpenAI回答を構造化データに変換"""
        try:
            lines = [line.strip() for line in response.split('\n') if line.strip()]
            
            question = ""
            options = []
            correct_answer = 0
            explanation = ""
            
            for line in lines:
                if line.startswith('問題:'):
                    question = line.replace('問題:', '').strip()
                elif line.startswith(('1.', '2.', '3.', '4.')):
                    options.append(line[2:].strip())
                elif line.startswith('正解:'):
                    try:
                        correct_answer = int(line.replace('正解:', '').strip()) - 1
                    except ValueError:
                        correct_answer = 0
                elif line.startswith('解説:'):
                    explanation = line.replace('解説:', '').strip()
            
            return {
                "question": question or "この場所について正しいものはどれでしょう？",
                "options": options if len(options) == 4 else [
                    "歴史的に重要な場所である",
                    "最近建設された建物である", 
                    "海外にある場所である",
                    "架空の場所である"
                ],
                "correct_answer": max(0, min(3, correct_answer)),
                "explanation": explanation or "歴史的に重要な場所として知られています。",
                "points": points
            }
            
        except Exception as e:
            logger.error(f"Quiz parsing error: {e}")
            return self._get_fallback_quiz(points)

    def _get_fallback_quiz(self, points: int) -> Dict:
        """OpenAI API失敗時のフォールバック"""
        return {
            "question": "この歴史スポットについて正しいものはどれでしょう？",
            "options": [
                "歴史的に重要な場所である",
                "最近建設された観光地である",
                "架空の場所である", 
                "海外にある場所である"
            ],
            "correct_answer": 0,
            "explanation": "多くの歴史スポットは長い歴史と文化的価値を持っています。",
            "points": points
        }

    async def get_usage_stats(self) -> Dict:
        """API使用状況の取得（コスト管理用）"""
        # 実装時はOpenAI APIの使用状況を取得
        return {
            "model": self.model,
            "estimated_cost_per_quiz": 0.001,  # 約0.1円/クイズ
            "current_settings": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
        }

# シングルトンインスタンス
openai_service = OpenAIService()