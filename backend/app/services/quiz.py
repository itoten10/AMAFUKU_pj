import random
from typing import Dict, Any, List

class QuizService:
    def __init__(self):
        self.quiz_templates = {
            "小学生": [
                {
                    "template": "{place}はいつ頃建てられたでしょう？",
                    "options_generator": self._generate_era_options_elementary,
                    "answer_generator": self._get_era_answer
                },
                {
                    "template": "{place}は何のための建物でしょう？",
                    "options_generator": self._generate_purpose_options_elementary,
                    "answer_generator": self._get_purpose_answer
                }
            ],
            "中学生": [
                {
                    "template": "{place}に関連する歴史上の人物は誰でしょう？",
                    "options_generator": self._generate_person_options_middle,
                    "answer_generator": self._get_person_answer
                },
                {
                    "template": "{place}が建てられた時代の特徴として正しいものはどれでしょう？",
                    "options_generator": self._generate_period_options_middle,
                    "answer_generator": self._get_period_answer
                }
            ],
            "高校生": [
                {
                    "template": "{place}の建築様式の特徴として正しいものはどれでしょう？",
                    "options_generator": self._generate_architecture_options_high,
                    "answer_generator": self._get_architecture_answer
                },
                {
                    "template": "{place}が歴史的に果たした役割として最も適切なものはどれでしょう？",
                    "options_generator": self._generate_role_options_high,
                    "answer_generator": self._get_role_answer
                }
            ]
        }
    
    async def generate_quiz(self, spot: Dict[str, Any], difficulty: str) -> Dict[str, Any]:
        templates = self.quiz_templates.get(difficulty, self.quiz_templates["中学生"])
        template = random.choice(templates)
        
        question = template["template"].format(place=spot['name'])
        options = template["options_generator"](spot)
        correct_answer = 0  # Always put correct answer first, then shuffle
        
        # Shuffle options while tracking correct answer
        indices = list(range(len(options)))
        random.shuffle(indices)
        shuffled_options = [options[i] for i in indices]
        correct_answer = indices.index(0)
        
        points = {"小学生": 10, "中学生": 15, "高校生": 20}.get(difficulty, 10)
        
        return {
            "spot_id": spot.get('place_id', 'unknown'),
            "spot_name": spot['name'],
            "question": question,
            "options": shuffled_options,
            "correct_answer": correct_answer,
            "explanation": template["answer_generator"](spot),
            "difficulty": difficulty,
            "points": points
        }
    
    def _generate_era_options_elementary(self, spot: Dict) -> List[str]:
        if "神社" in spot['name'] or "shrine" in spot.get('types', []):
            return ["平安時代", "江戸時代", "明治時代", "昭和時代"]
        elif "寺" in spot['name'] or "temple" in spot.get('types', []):
            return ["奈良時代", "鎌倉時代", "室町時代", "江戸時代"]
        else:
            return ["古墳時代", "平安時代", "戦国時代", "江戸時代"]
    
    def _get_era_answer(self, spot: Dict) -> str:
        if "神社" in spot['name']:
            return "この神社は平安時代に創建されたと伝えられています。当時の貴族たちの信仰を集めていました。"
        elif "寺" in spot['name']:
            return "このお寺は奈良時代に建立されました。仏教が日本に広まった重要な時期の建築物です。"
        else:
            return "この史跡は長い歴史を持ち、複数の時代にわたって重要な役割を果たしてきました。"
    
    def _generate_purpose_options_elementary(self, spot: Dict) -> List[str]:
        if "神社" in spot['name']:
            return ["神様をまつる場所", "お殿様の家", "学校", "市場"]
        elif "寺" in spot['name']:
            return ["仏様をまつる場所", "武士の訓練場", "商人の店", "農民の家"]
        else:
            return ["歴史的な建造物", "遊園地", "工場", "駅"]
    
    def _get_purpose_answer(self, spot: Dict) -> str:
        if "神社" in spot['name']:
            return "神社は神様をまつり、人々がお参りをする神聖な場所です。"
        elif "寺" in spot['name']:
            return "お寺は仏様をまつり、僧侶が修行をする場所です。"
        else:
            return "この場所は歴史的に重要な役割を果たしてきました。"
    
    def _generate_person_options_middle(self, spot: Dict) -> List[str]:
        return ["源頼朝", "織田信長", "豊臣秀吉", "徳川家康"]
    
    def _get_person_answer(self, spot: Dict) -> str:
        return "源頼朝は鎌倉幕府を開いた武将で、この地域の発展に大きく貢献しました。"
    
    def _generate_period_options_middle(self, spot: Dict) -> List[str]:
        return [
            "武士が政治の中心になった",
            "天皇が直接政治を行った",
            "外国人が日本を支配した",
            "農民が政治を動かした"
        ]
    
    def _get_period_answer(self, spot: Dict) -> str:
        return "この時代は武士が台頭し、政治の実権を握るようになった重要な転換期でした。"
    
    def _generate_architecture_options_high(self, spot: Dict) -> List[str]:
        return [
            "寝殿造りの特徴を持つ",
            "書院造りの様式",
            "西洋建築の影響",
            "モダニズム建築"
        ]
    
    def _get_architecture_answer(self, spot: Dict) -> str:
        return "この建築物は日本の伝統的な建築様式の特徴をよく表しています。"
    
    def _generate_role_options_high(self, spot: Dict) -> List[str]:
        return [
            "地域の政治・経済の中心",
            "純粋な娯楽施設",
            "外国との貿易拠点",
            "軍事訓練施設"
        ]
    
    def _get_role_answer(self, spot: Dict) -> str:
        return "この場所は地域の政治・経済・文化の中心として重要な役割を果たしてきました。"

quiz_service = QuizService()