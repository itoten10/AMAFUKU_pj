# historical_quiz.py
import googlemaps
import random
import requests
from typing import List, Dict, Tuple
import re

class HistoricalQuizGenerator:
    def __init__(self, gmaps_client):
        self.gmaps = gmaps_client
        
    def get_historical_spots_along_route(self, route_coords: List[Tuple[float, float]], num_points: int = 5) -> List[Dict]:
        """ルート上の歴史的スポットを取得"""
        historical_spots = []
        
        # 型チェックと変換
        if not route_coords:
            print("警告: route_coordsが空です")
            return []
    
        # route_coordsが正しい形式か確認
        if isinstance(route_coords[0], (list, tuple)) and len(route_coords[0]) == 2:
            # 正しい形式
            pass
        else:
            print(f"警告: route_coordsの形式が不正です: {type(route_coords[0])}")
            return []
        
        # ルートを等間隔でサンプリング
        step = max(1, len(route_coords) // num_points)
        sample_points = route_coords[::step]
        
        # 各ポイント周辺の歴史的スポットを検索
        search_types = [
            'tourist_attraction',
            'museum', 
            'church',
            'hindu_temple',
            'buddhist_temple',
            'castle',
            'monument'
        ]
        
        for point in sample_points:
            for search_type in search_types:
                try:
                    # Places API で周辺検索（typesの代わりにtypeを使用）
                    results = self.gmaps.places_nearby(
                        location=point,
                        radius=3000,  # 3km圏内
                        type=search_type,  # 修正: typesではなくtype
                        language='ja'
                    )
                    
                    for place in results.get('results', [])[:2]:  # 各地点から最大2件
                        # 詳細情報を取得（fieldsを修正）
                        try:
                            place_details = self.gmaps.place(
                                place['place_id'],
                                language='ja',
                                fields=['name', 'geometry', 'type', 'formatted_address', 'url', 'website']  # 修正: typesをtypeに変更、editorial_summaryを削除
                            )
                            
                            if 'result' in place_details:
                                detail = place_details['result']
                                spot = {
                                    'id': place['place_id'],
                                    'name': place['name'],
                                    'lat': place['geometry']['location']['lat'],
                                    'lng': place['geometry']['location']['lng'],
                                    'types': place.get('types', []),  # 元のplaceオブジェクトから取得
                                    'address': detail.get('formatted_address', ''),
                                    'description': self._generate_description(place['name'], place.get('types', [])),
                                    'difficulty': self._determine_difficulty(place['name'])
                                }
                                
                                # 重複チェック
                                if not any(s['id'] == spot['id'] for s in historical_spots):
                                    historical_spots.append(spot)
                                    
                        except Exception as e:
                            # 個別のplace詳細取得エラーは無視して続行
                            print(f"Error fetching place details: {e}")
                            continue
                            
                except Exception as e:
                    print(f"Error fetching places nearby: {e}")
                    continue
                    
        return historical_spots[:10]  # 最大10件まで
    
    def _generate_description(self, name: str, types: List[str]) -> str:
        """スポットの簡単な説明を生成"""
        descriptions = {
            'hindu_temple': f"{name}はヒンドゥー教の寺院です。",
            'buddhist_temple': f"{name}は仏教寺院です。",
            'shinto_shrine': f"{name}は神社です。",
            'church': f"{name}は教会です。",
            'museum': f"{name}では貴重な歴史資料を見ることができます。",
            'castle': f"{name}は歴史的な城・城跡です。",
            'monument': f"{name}は歴史的な記念碑です。",
            'tourist_attraction': f"{name}は人気の観光スポットです。"
        }
        
        # 日本語での判定も追加
        if '寺' in name or '院' in name:
            return f"{name}は歴史ある寺院です。"
        elif '神社' in name or '宮' in name:
            return f"{name}は地域の信仰を集める神社です。"
        elif '城' in name:
            return f"{name}は歴史的な城跡です。"
        elif '美術館' in name or '博物館' in name:
            return f"{name}では貴重な展示を見ることができます。"
        
        # typesから判定
        for spot_type, desc in descriptions.items():
            if spot_type in types:
                return desc
                
        return f"{name}は歴史的な観光スポットです。"
    
    def _determine_difficulty(self, name: str) -> str:
        """難易度を判定"""
        # 簡易的な判定（実際は内容に基づいて判定）
        if any(word in name for word in ['城', '寺', '神社', '大']):
            return "小学生"
        elif any(word in name for word in ['美術館', '博物館']):
            return "中学生"
        else:
            return "高校生"
    
    def generate_quiz(self, spot: Dict, difficulty: str = "中学生") -> Dict:
        """スポットに関するクイズを生成"""
        quiz_templates = {
            "小学生": [
                {
                    "question": f"{spot['name']}はどこにありますか？",
                    "options": self._generate_location_options(spot),
                    "correct": 0,
                    "explanation": f"{spot['name']}は{spot['address']}にあります。"
                },
                {
                    "question": f"{spot['name']}は何でしょう？",
                    "options": self._generate_type_options(spot),
                    "correct": 0,
                    "explanation": spot['description']
                }
            ],
            "中学生": [
                {
                    "question": f"{spot['name']}に関する正しい説明はどれですか？",
                    "options": self._generate_description_options(spot),
                    "correct": 0,
                    "explanation": f"正解！{spot['description']}"
                }
            ],
            "高校生": [
                {
                    "question": f"{spot['name']}の歴史的意義について、最も適切なものを選びなさい。",
                    "options": self._generate_advanced_options(spot),
                    "correct": 0,
                    "explanation": f"{spot['name']}は地域の歴史において重要な役割を果たしました。"
                }
            ]
        }
        
        # 難易度に応じたクイズを選択
        quiz_list = quiz_templates.get(difficulty, quiz_templates["中学生"])
        quiz = random.choice(quiz_list)
        
        # オプションをシャッフル
        options = quiz['options']
        correct_answer = options[0]  # 最初が正解
        random.shuffle(options)
        
        # 正解のインデックスを更新
        quiz['correct'] = options.index(correct_answer)
        
        return {
            'spot_name': spot['name'],
            'question': quiz['question'],
            'options': options,
            'correct': quiz['correct'],
            'explanation': quiz['explanation'],
            'points': {'小学生': 10, '中学生': 20, '高校生': 30}.get(difficulty, 10)
        }
    
    def _generate_location_options(self, spot: Dict) -> List[str]:
        """位置に関する選択肢を生成"""
        address_parts = spot['address'].split('、')
        if len(address_parts) > 0:
            # 実際の住所から都道府県や市区町村を抽出
            correct = "この付近"
            if '東京都' in spot['address']:
                correct = "東京都内"
            elif '神奈川県' in spot['address']:
                correct = "神奈川県内"
            elif '千葉県' in spot['address']:
                correct = "千葉県内"
            elif '埼玉県' in spot['address']:
                correct = "埼玉県内"
                
            options = [correct, "北海道", "大阪府", "福岡県"]
            return options[:4]
        return ["この場所", "別の場所", "遠い場所", "近い場所"]
    
    def _generate_type_options(self, spot: Dict) -> List[str]:
        """種類に関する選択肢を生成"""
        type_mapping = {
            'hindu_temple': 'ヒンドゥー寺院',
            'buddhist_temple': '仏教寺院',
            'shinto_shrine': '神社',
            'church': '教会',
            'museum': '博物館',
            'castle': '城',
            'park': '公園',
            'tourist_attraction': '観光地'
        }
        
        # 名前から推測
        correct = "観光地"
        if '寺' in spot['name'] or '院' in spot['name']:
            correct = '寺院'
        elif '神社' in spot['name'] or '宮' in spot['name']:
            correct = '神社'
        elif '城' in spot['name']:
            correct = '城'
        elif '美術館' in spot['name']:
            correct = '美術館'
        elif '博物館' in spot['name']:
            correct = '博物館'
        else:
            # typesから判定
            for t in spot.get('types', []):
                if t in type_mapping:
                    correct = type_mapping[t]
                    break
                    
        options = [correct]
        all_types = ['寺院', '神社', '城', '美術館', '博物館', '公園', 'ショッピングモール', 'オフィスビル']
        # correctを除外してランダムに3つ選択
        other_types = [t for t in all_types if t != correct]
        options.extend(random.sample(other_types, min(3, len(other_types))))
        
        return options[:4]
    
    def _generate_description_options(self, spot: Dict) -> List[str]:
        """説明に関する選択肢を生成"""
        correct = spot['description']
        wrong_options = [
            "最近建てられた商業施設です。",
            "江戸時代の大名屋敷跡です。",
            "明治時代の産業遺産です。",
            "昭和時代に作られた公園です。",
            "平成時代の文化施設です。"
        ]
        # 正解と異なる選択肢を3つ選ぶ
        selected_wrong = random.sample(wrong_options, 3)
        return [correct] + selected_wrong
    
    def _generate_advanced_options(self, spot: Dict) -> List[str]:
        """高度な選択肢を生成"""
        options = [
            "地域の文化的中心として機能してきた",
            "経済発展の象徴として建設された",
            "防衛上の要衝として重要だった",
            "外交上の拠点として使用された",
            "宗教的な巡礼地として栄えた",
            "教育機関として地域に貢献した"
        ]
        return random.sample(options, 4)
    