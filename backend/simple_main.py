from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 最小限のFastAPIアプリ
app = FastAPI(title="Famoly Drive API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# テスト用の基本エンドポイント
@app.get("/")
async def root():
    return {"message": "Welcome to Famoly Drive API"}

# ヘルスチェック
@app.get("/health")
async def health_check():
    return {"status": "healthy", "google_maps_api": bool(os.getenv("GOOGLE_MAPS_API_KEY"))}

# 仮のルート検索エンドポイント
@app.post("/api/v1/routes/search")
async def search_route(route_data: dict):
    origin = route_data.get("origin", "東京駅")
    destination = route_data.get("destination", "鎌倉駅")
    
    # 仮のデータを返す
    return {
        "route": {
            "origin": origin,
            "destination": destination,
            "origin_coords": {"lat": 35.6812, "lng": 139.7671},
            "dest_coords": {"lat": 35.3197, "lng": 139.5516},
            "distance": "55.2 km",
            "duration": "1時間 15分",
            "polyline": "sample_polyline_data"
        },
        "historical_spots": [
            {
                "place_id": "sample_1",
                "name": "鎌倉大仏",
                "address": "神奈川県鎌倉市長谷",
                "lat": 35.3169,
                "lng": 139.5359,
                "types": ["tourist_attraction"],
                "description": "鎌倉大仏は13世紀に建立された国宝の仏像です。"
            },
            {
                "place_id": "sample_2", 
                "name": "鶴岡八幡宮",
                "address": "神奈川県鎌倉市雪ノ下",
                "lat": 35.3249,
                "lng": 139.5565,
                "types": ["shrine"],
                "description": "鶴岡八幡宮は鎌倉の守護神として古くから信仰されています。"
            }
        ]
    }

# 仮のクイズ生成エンドポイント
@app.post("/api/v1/quizzes/generate")
async def generate_quiz(spot_data: dict, difficulty: str = "中学生"):
    spot_name = spot_data.get("name", "歴史スポット")
    
    return {
        "spot_id": spot_data.get("place_id", "sample_1"),
        "spot_name": spot_name,
        "question": f"{spot_name}について正しいものはどれでしょう？",
        "options": [
            f"{spot_name}は鎌倉時代に建立されました",
            f"{spot_name}は江戸時代に建立されました", 
            f"{spot_name}は明治時代に建立されました",
            f"{spot_name}は昭和時代に建立されました"
        ],
        "correct_answer": 0,
        "explanation": f"{spot_name}は鎌倉時代に建立された歴史ある建造物です。",
        "difficulty": difficulty,
        "points": 10
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)