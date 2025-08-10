'use client'

import { useState } from 'react'
import { GoogleMapRoute } from '@/components/GoogleMapRoute'
import { SampleMapRoute } from '@/components/SampleMapRoute'
import { WorkingQuizPanel } from '@/components/WorkingQuizPanel'
import { TrendingUp } from 'lucide-react'

interface RouteInfo {
  origin: string
  destination: string
  distance: string
  duration: string
  route: google.maps.DirectionsRoute | null
}

interface HistoricalSpot {
  place_id: string
  name: string
  address: string
  lat: number
  lng: number
  description: string
}

export default function Home() {
  const [currentRoute, setCurrentRoute] = useState<RouteInfo | null>(null)
  const [historicalSpots, setHistoricalSpots] = useState<HistoricalSpot[]>([])
  const [selectedSpot, setSelectedSpot] = useState<HistoricalSpot | null>(null)
  const [userScore, setUserScore] = useState(0)
  const [isGoogleMapsAvailable, setIsGoogleMapsAvailable] = useState(false)

  // Google Maps APIの可用性をチェック（現在は無効化してサンプルモードを使用）
  useState(() => {
    // Google Maps APIが設定されていない、または有効化されていない場合はサンプルモードを使用
    setIsGoogleMapsAvailable(true) // 一時的にfalseに固定してサンプルモードを使用
  })

  const handleRouteFound = (routeInfo: RouteInfo) => {
    setCurrentRoute(routeInfo)
    setSelectedSpot(null) // ルートが変わったらクイズパネルをリセット
  }

  const handleSpotsFound = (spots: HistoricalSpot[]) => {
    setHistoricalSpots(spots)
  }

  const handleScoreUpdate = (points: number) => {
    setUserScore(prev => prev + points)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-blue-600 rounded"></div>
              <h1 className="text-xl font-bold text-gray-900">
                Famoly Drive
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                あなたのスコア: <span className="font-bold text-blue-600">{userScore}点</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 左側: ルート検索と地図 */}
          <div className="lg:col-span-2">
            {isGoogleMapsAvailable ? (
              <GoogleMapRoute 
                onRouteFound={handleRouteFound}
                onSpotsFound={handleSpotsFound}
              />
            ) : (
              <SampleMapRoute 
                onRouteFound={handleRouteFound}
                onSpotsFound={handleSpotsFound}
              />
            )}
            
            {/* ルート情報表示 */}
            {currentRoute && (
              <div className="mt-4 bg-white rounded-lg shadow-md p-4">
                <h3 className="font-semibold mb-2">ルート情報</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">出発:</span> {currentRoute.origin}
                  </div>
                  <div>
                    <span className="text-gray-600">到着:</span> {currentRoute.destination}
                  </div>
                  <div>
                    <span className="text-gray-600">距離:</span> {currentRoute.distance}
                  </div>
                  <div>
                    <span className="text-gray-600">時間:</span> {currentRoute.duration}
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* 右側: スコアボードと歴史スポット/クイズ */}
          <div className="space-y-6">
            {/* スコアボード */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
                ランキング
              </h2>
              <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">あなたのスコア</span>
                  <span className="text-2xl font-bold text-blue-600">{userScore}点</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg font-semibold text-yellow-500">1位</span>
                    <span className="font-medium">たろう</span>
                  </div>
                  <span className="font-semibold">580点</span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg font-semibold text-gray-400">2位</span>
                    <span className="font-medium">はなこ</span>
                  </div>
                  <span className="font-semibold">450点</span>
                </div>
                {userScore > 0 && (
                  <div className="flex items-center justify-between p-3 rounded-lg bg-blue-100 border border-blue-300">
                    <div className="flex items-center space-x-3">
                      <span className="text-lg font-semibold text-blue-600">3位</span>
                      <span className="font-medium">あなた</span>
                    </div>
                    <span className="font-semibold">{userScore}点</span>
                  </div>
                )}
              </div>
            </div>

            {/* 歴史スポット一覧 */}
            {historicalSpots.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-lg font-semibold mb-4">歴史スポット</h2>
                <div className="space-y-2">
                  {historicalSpots.map((spot) => (
                    <button
                      key={spot.place_id}
                      onClick={() => setSelectedSpot(spot)}
                      className={`w-full text-left p-3 rounded-lg border transition ${
                        selectedSpot?.place_id === spot.place_id
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      <div className="font-medium text-gray-900">{spot.name}</div>
                      <div className="text-sm text-gray-500">{spot.address}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* クイズパネル */}
            {selectedSpot && (
              <WorkingQuizPanel 
                spot={selectedSpot}
                onScoreUpdate={handleScoreUpdate}
              />
            )}

            {/* デフォルトメッセージ */}
            {!selectedSpot && historicalSpots.length === 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-lg font-semibold mb-4">クイズ</h2>
                <div className="text-center text-gray-500">
                  <div className="text-4xl mb-4">🎯</div>
                  <p>ルート検索をして</p>
                  <p>歴史スポットを見つけましょう！</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}