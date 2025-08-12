# historical_data.py
import requests
import random

def get_historical_points(route_coords):
    """ルート沿いの歴史的スポットを取得（MVP版は仮データ）"""
    
    # MVP版: 仮の歴史データ
    sample_historical_data = [
        {
            "name": "源頼朝の挙兵地",
            "lat": 35.3194,
            "lng": 139.5466,
            "description": "1180年、源頼朝が平家打倒の兵を挙げた歴史的な場所",
            "year": "1180年",
            "category": "鎌倉時代"
        },
        {
            "name": "東海道五十三次 - 神奈川宿",
            "lat": 35.4659,
            "lng": 139.6239,
            "description": "江戸時代の重要な宿場町。浮世絵にも描かれた",
            "year": "1601年",
            "category": "江戸時代"
        }
    ]
    
    # 実際のプロダクトではWikipedia APIなどと連携
    return sample_historical_data

def add_historical_markers(map_obj, historical_points):
    """歴史ポイントをマップに追加"""
    for point in historical_points:
        folium.Marker(
            [point['lat'], point['lng']],
            popup=folium.Popup(
                f"""
                <b>{point['name']}</b><br>
                <i>{point['year']}</i><br>
                {point['description']}
                """,
                max_width=300
            ),
            icon=folium.Icon(color='orange', icon='info-sign')
        ).add_to(map_obj)