# utils.py
import folium
import polyline

def create_route_map(route_data, origin_coords, dest_coords):
    """ルートを含む地図を作成"""
    # 地図の中心を計算
    center_lat = (origin_coords[0] + dest_coords[0]) / 2
    center_lng = (origin_coords[1] + dest_coords[1]) / 2
    
    # 地図作成
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # ルートを描画
    route_coords = polyline.decode(route_data['overview_polyline'])
    folium.PolyLine(
        route_coords,
        color='blue',
        weight=5,
        opacity=0.8
    ).add_to(m)
    
    # 出発地と目的地のマーカー
    folium.Marker(
        origin_coords,
        popup=f"出発: {origin}",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        dest_coords,
        popup=f"到着: {destination}",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    return m