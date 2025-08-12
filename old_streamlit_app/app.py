import streamlit as st
import folium
from streamlit_folium import st_folium
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
import polyline
from historical_quiz import HistoricalQuizGenerator

# 環境変数読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="Famoly Drive",
    page_icon="🚗",
    layout="wide"
)

# Google Maps クライアント初期化
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
quiz_generator = HistoricalQuizGenerator(gmaps)

# タイトル
st.title("🚗 Famoly Drive")
st.markdown("移動時間を学習時間に変える、新しい家族体験")

# セッション状態の初期化
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'answered_quizzes' not in st.session_state:
    st.session_state.answered_quizzes = set()

# スコア表示
col_score1, col_score2, col_score3 = st.columns([3, 1, 1])
with col_score2:
    st.metric("🏆 スコア", f"{st.session_state.quiz_score}点")
with col_score3:
    if st.button("リセット"):
        st.session_state.quiz_score = 0
        st.session_state.answered_quizzes = set()

# 入力フォーム
col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("🏠 出発地", "東京駅")
    
with col2:
    destination = st.text_input("🎯 目的地", "鎌倉駅")

# ルート検索ボタン
if st.button("🔍 ルート検索", type="primary"):
    if origin and destination:
        with st.spinner("ルートを検索中..."):
            try:
                # Geocoding APIで座標取得
                origin_geocode = gmaps.geocode(origin, language='ja')
                dest_geocode = gmaps.geocode(destination, language='ja')
                
                if origin_geocode and dest_geocode:
                    # 座標を取得
                    origin_coords = (
                        origin_geocode[0]['geometry']['location']['lat'],
                        origin_geocode[0]['geometry']['location']['lng']
                    )
                    dest_coords = (
                        dest_geocode[0]['geometry']['location']['lat'],
                        dest_geocode[0]['geometry']['location']['lng']
                    )
                    
                    # Directions APIでルート取得
                    directions = gmaps.directions(
                        origin,
                        destination,
                        mode="driving",
                        language="ja",
                        departure_time=datetime.now()
                    )
                    
                    if directions:
                        route = directions[0]
                        
                        # ルート情報を表示
                        st.success("✅ ルートが見つかりました！")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("距離", route['legs'][0]['distance']['text'])
                        with col2:
                            st.metric("所要時間", route['legs'][0]['duration']['text'])
                        with col3:
                            st.metric("経由地点", f"{len(route['legs'][0]['steps'])}箇所")
                        
                        # 地図の作成
                        st.subheader("🗺️ ルートマップ")
                        
                        # 地図の中心を計算
                        center_lat = (origin_coords[0] + dest_coords[0]) / 2
                        center_lng = (origin_coords[1] + dest_coords[1]) / 2
                        
                        # Foliumで地図作成
                        m = folium.Map(
                            location=[center_lat, center_lng],
                            zoom_start=10
                        )
                        
                        # ルートを描画
                        route_polyline = route['overview_polyline']['points']
                        route_coords = polyline.decode(route_polyline)
                        
                        folium.PolyLine(
                            route_coords,
                            color='blue',
                            weight=5,
                            opacity=0.8
                        ).add_to(m)
                        
                        # 出発地マーカー
                        folium.Marker(
                            origin_coords,
                            popup=f"出発: {origin}",
                            icon=folium.Icon(color='green', icon='play', prefix='fa'),
                            tooltip="出発地"
                        ).add_to(m)
                        
                        # 目的地マーカー
                        folium.Marker(
                            dest_coords,
                            popup=f"到着: {destination}",
                            icon=folium.Icon(color='red', icon='stop', prefix='fa'),
                            tooltip="目的地"
                        ).add_to(m)
                        
                        # 実際の歴史スポットを取得
                        with st.spinner("歴史スポットを検索中..."):
                            try:
                                historical_spots = quiz_generator.get_historical_spots_along_route(
                                    route_coords,
                                    num_points=5
                                )
                                st.success(f"✅ {len(historical_spots)}件の歴史スポットが見つかりました！")
                            except Exception as e:
                                st.warning(f"歴史スポットの取得中にエラーが発生しました: {str(e)}")
                                historical_spots = []
                        
                        # 歴史スポットが0件の場合は仮データを使用
                        if len(historical_spots) == 0:
                            st.info("周辺に歴史スポットが見つかりませんでした。サンプルデータを表示します。")
                            historical_spots = [
                                {
                                    'id': 'sample1',
                                    'name': '皇居',
                                    'lat': 35.6852,
                                    'lng': 139.7528,
                                    'types': ['tourist_attraction'],
                                    'address': '東京都千代田区千代田1-1',
                                    'description': '皇居は江戸城の跡地で、現在は天皇の居住地です。',
                                    'difficulty': '小学生'
                                },
                                {
                                    'id': 'sample2',
                                    'name': '鎌倉大仏',
                                    'lat': 35.3169,
                                    'lng': 139.5359,
                                    'types': ['buddhist_temple'],
                                    'address': '神奈川県鎌倉市長谷4-2-28',
                                    'description': '鎌倉大仏は13世紀に建立された国宝の仏像です。',
                                    'difficulty': '中学生'
                                }
                            ]
                        
                        # 歴史スポットをマップに追加
                        for i, spot in enumerate(historical_spots):
                            folium.Marker(
                                [spot['lat'], spot['lng']],
                                popup=folium.Popup(
                                    f"<b>{spot['name']}</b><br>"
                                    f"<i>{spot['address']}</i><br>"
                                    f"{spot['description']}",
                                    max_width=250
                                ),
                                icon=folium.Icon(
                                    color='orange', 
                                    icon='landmark', 
                                    prefix='fa'
                                ),
                                tooltip=f"📍 {spot['name']}"
                            ).add_to(m)
                        
                        # 地図を表示（ここが重要！）
                        map_data = st_folium(m, height=500, returned_objects=["last_object_clicked"])
                        
                        # ルート詳細
                        with st.expander("📍 ルート詳細"):
                            for i, step in enumerate(route['legs'][0]['steps'][:5]):
                                st.write(f"{i+1}. {step['html_instructions']}")
                                st.write(f"   距離: {step['distance']['text']}, 時間: {step['duration']['text']}")
                        
                        # 歴史スポット一覧とクイズ
                        st.subheader("📚 ルート周辺の歴史スポット")
                        
                        # 難易度選択
                        selected_difficulty = st.selectbox(
                            "クイズの難易度を選択",
                            ["小学生", "中学生", "高校生"],
                            index=1
                        )
                        
                        for i, spot in enumerate(historical_spots):
                            with st.expander(f"🏛️ {spot['name']}"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.write(f"📍 **住所**: {spot['address']}")
                                    st.write(f"📝 **説明**: {spot['description']}")
                                    
                                with col2:
                                    # Google Maps へのリンク
                                    maps_url = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lng']}"
                                    st.markdown(f"[🗺️ Google Mapsで見る]({maps_url})")
                                
                                # クイズセクション
                                st.markdown("---")
                                quiz_key = f"quiz_{spot['id']}"
                                
                                if quiz_key not in st.session_state.answered_quizzes:
                                    if st.button(f"🎯 クイズに挑戦！", key=f"btn_{quiz_key}"):
                                        # クイズを生成
                                        quiz = quiz_generator.generate_quiz(spot, selected_difficulty)
                                        st.session_state[f"current_quiz_{quiz_key}"] = quiz
                                
                                # クイズが生成されている場合は表示
                                if f"current_quiz_{quiz_key}" in st.session_state:
                                    quiz = st.session_state[f"current_quiz_{quiz_key}"]
                                    
                                    st.markdown(f"**Q: {quiz['question']}**")
                                    
                                    # 選択肢を表示
                                    answer = st.radio(
                                        "答えを選んでください：",
                                        options=quiz['options'],
                                        key=f"radio_{quiz_key}"
                                    )
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button("回答する", key=f"answer_{quiz_key}"):
                                            selected_index = quiz['options'].index(answer)
                                            
                                            if selected_index == quiz['correct']:
                                                st.success(f"🎉 正解！ +{quiz['points']}ポイント!")
                                                st.info(f"💡 {quiz['explanation']}")
                                                st.session_state.quiz_score += quiz['points']
                                                st.session_state.answered_quizzes.add(quiz_key)
                                                st.balloons()
                                                # クイズを削除
                                                del st.session_state[f"current_quiz_{quiz_key}"]
                                                st.rerun()
                                            else:
                                                st.error("❌ 不正解... もう一度考えてみよう！")
                                                st.info(f"ヒント: {quiz['explanation'][:20]}...")
                                    
                                    with col2:
                                        if st.button("スキップ", key=f"skip_{quiz_key}"):
                                            st.session_state.answered_quizzes.add(quiz_key)
                                            del st.session_state[f"current_quiz_{quiz_key}"]
                                            st.rerun()
                                
                                elif quiz_key in st.session_state.answered_quizzes:
                                    st.info("✅ このクイズは回答済みです")
                    
                else:
                    st.error("❌ 場所が見つかりませんでした。地名を確認してください。")
                    
            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")
                st.info("💡 ヒント: Google Maps APIキーが正しく設定されているか確認してください。")
    else:
        st.warning("⚠️ 出発地と目的地を入力してください。")

# サイドバー
with st.sidebar:
    st.header("📚 学習設定")
    
    difficulty = st.select_slider(
        "難易度",
        options=["小学生", "中学生", "高校生", "大人"],
        value="中学生"
    )
    
    st.header("ℹ️ 使い方")
    st.info("""
    1. 出発地と目的地を入力
    2. ルート検索をクリック
    3. 地図上の歴史スポットを確認
    4. クイズに挑戦してポイントゲット！
    """)
    
    st.header("🔧 デバッグ情報")
    if os.getenv('GOOGLE_MAPS_API_KEY'):
        st.success("✅ APIキー: 設定済み")
    else:
        st.error("❌ APIキー: 未設定")
    
    st.markdown("---")
    st.header("🏆 ランキング")
    
    # 仮のランキングデータ
    rankings = [
        {"name": "たろう", "score": 580},
        {"name": "はなこ", "score": 450},
        {"name": "あなた", "score": st.session_state.quiz_score},
        {"name": "じろう", "score": 320},
        {"name": "さぶろう", "score": 280}
    ]
    
    rankings.sort(key=lambda x: x['score'], reverse=True)
    
    for i, player in enumerate(rankings[:5]):
        if player['name'] == "あなた":
            st.sidebar.markdown(f"**{i+1}位: {player['name']} - {player['score']}点** ⭐")
        else:
            st.sidebar.markdown(f"{i+1}位: {player['name']} - {player['score']}点")