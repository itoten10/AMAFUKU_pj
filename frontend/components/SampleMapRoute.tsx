'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'

interface RouteInfo {
  origin: string
  destination: string
  distance: string
  duration: string
  route: null
}

interface HistoricalSpot {
  place_id: string
  name: string
  address: string
  lat: number
  lng: number
  description: string
}

interface SampleMapRouteProps {
  onRouteFound: (routeInfo: RouteInfo) => void
  onSpotsFound: (spots: HistoricalSpot[]) => void
}

export function SampleMapRoute({ onRouteFound, onSpotsFound }: SampleMapRouteProps) {
  const [origin, setOrigin] = useState('東京駅')
  const [destination, setDestination] = useState('鎌倉駅')
  const [loading, setLoading] = useState(false)

  const searchRoute = () => {
    if (!origin.trim() || !destination.trim()) {
      toast.error('出発地と目的地を入力してください')
      return
    }

    setLoading(true)

    // サンプルデータでルート検索をシミュレート
    setTimeout(() => {
      const routeInfo: RouteInfo = {
        origin,
        destination,
        distance: getDistance(origin, destination),
        duration: getDuration(origin, destination),
        route: null
      }

      const spots = getSampleHistoricalSpots(origin, destination)

      onRouteFound(routeInfo)
      onSpotsFound(spots)
      
      toast.success('ルートが見つかりました！（サンプルデータ）')
      setLoading(false)
    }, 1500)
  }

  const getDistance = (origin: string, destination: string): string => {
    const distances: { [key: string]: string } = {
      '東京駅-鎌倉駅': '51.2 km',
      '新宿-鎌倉': '48.3 km', 
      '渋谷-鎌倉': '45.7 km',
      '東京-京都': '381.2 km',
      '東京-大阪': '403.5 km'
    }
    
    const key = `${origin}-${destination}`
    return distances[key] || `${Math.floor(Math.random() * 100 + 20)} km`
  }

  const getDuration = (origin: string, destination: string): string => {
    const durations: { [key: string]: string } = {
      '東京駅-鎌倉駅': '1時間 12分',
      '新宿-鎌倉': '1時間 8分',
      '渋谷-鎌倉': '1時間 2分', 
      '東京-京都': '5時間 23分',
      '東京-大阪': '6時間 12分'
    }
    
    const key = `${origin}-${destination}`
    return durations[key] || `${Math.floor(Math.random() * 3 + 1)}時間 ${Math.floor(Math.random() * 60)}分`
  }

  const getSampleHistoricalSpots = (origin: string, destination: string): HistoricalSpot[] => {
    // 出発地・目的地に基づいてサンプルスポットを変更
    if (destination.includes('鎌倉')) {
      return [
        {
          place_id: 'sample_1',
          name: '鎌倉大仏',
          address: '神奈川県鎌倉市長谷4-2-28',
          lat: 35.3169,
          lng: 139.5359,
          description: '鎌倉大仏は13世紀に建立された国宝の仏像です。高さ11.3メートルの青銅製阿弥陀如来坐像で、日本を代表する文化遺産の一つです。'
        },
        {
          place_id: 'sample_2',
          name: '鶴岡八幡宮',
          address: '神奈川県鎌倉市雪ノ下2-1-31',
          lat: 35.3249,
          lng: 139.5565,
          description: '鶴岡八幡宮は源頼朝によって現在地に遷された鎌倉の象徴的な神社です。鎌倉幕府の宗廟として崇敬されました。'
        },
        {
          place_id: 'sample_3',
          name: '建長寺',
          address: '神奈川県鎌倉市山ノ内8',
          lat: 35.3374,
          lng: 139.5526,
          description: '建長寺は1253年に創建された日本最古の禅寺です。臨済宗建長寺派の大本山として知られています。'
        },
        {
          place_id: 'sample_4',
          name: '円覚寺',
          address: '神奈川県鎌倉市山ノ内409',
          lat: 35.3376,
          lng: 139.5479,
          description: '円覚寺は1282年に北条時宗が創建した臨済宗円覚寺派の大本山です。美しい庭園でも有名です。'
        },
        {
          place_id: 'sample_5',
          name: '銭洗弁財天宇賀福神社',
          address: '神奈川県鎌倉市佐助2-25-16',
          lat: 35.3190,
          lng: 139.5448,
          description: '銭洗弁財天は洞窟の中にある神社で、ここの湧水でお金を洗うと何倍にもなって返ってくると信仰されています。'
        }
      ]
    } else if (destination.includes('京都')) {
      return [
        {
          place_id: 'sample_kyoto_1',
          name: '清水寺',
          address: '京都府京都市東山区清水1-294',
          lat: 34.9949,
          lng: 135.7849,
          description: '清水寺は778年に創建された京都を代表する寺院です。清水の舞台で有名な本堂は国宝に指定されています。'
        },
        {
          place_id: 'sample_kyoto_2',
          name: '金閣寺',
          address: '京都府京都市北区金閣寺町1',
          lat: 35.0394,
          lng: 135.7292,
          description: '金閣寺（鹿苑寺）は1397年に足利義満が建立した金色に輝く三層の楼閣建築で、京都の象徴的存在です。'
        },
        {
          place_id: 'sample_kyoto_3',
          name: '伏見稲荷大社',
          address: '京都府京都市伏見区深草藪之内町68',
          lat: 34.9671,
          lng: 135.7727,
          description: '伏見稲荷大社は全国に約3万社ある稲荷神社の総本宮です。千本鳥居で有名な山全体が神域となっています。'
        }
      ]
    } else {
      return [
        {
          place_id: 'sample_default_1',
          name: '浅草寺',
          address: '東京都台東区浅草2-3-1',
          lat: 35.7148,
          lng: 139.7967,
          description: '浅草寺は645年に創建された東京最古の寺院です。雷門と仲見世通りで有名な観光地です。'
        },
        {
          place_id: 'sample_default_2',
          name: '明治神宮',
          address: '東京都渋谷区代々木神園町1-1',
          lat: 35.6763,
          lng: 139.6993,
          description: '明治神宮は明治天皇と昭憲皇太后を祀る神社です。都心にありながら豊かな森に囲まれた神聖な空間です。'
        },
        {
          place_id: 'sample_default_3',
          name: '東京国立博物館',
          address: '東京都台東区上野公園13-9',
          lat: 35.7188,
          lng: 139.7753,
          description: '東京国立博物館は日本最古の博物館で、日本を中心とした東洋の文化財を収集・保管・展示しています。'
        }
      ]
    }
  }

  return (
    <div className="space-y-6">
      {/* ルート検索フォーム */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">ルート検索（サンプルモード）</h2>
        <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            ⚠️ Google Maps APIが設定されていません。サンプルデータで動作確認できます。
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              出発地
            </label>
            <input
              type="text"
              value={origin}
              onChange={(e) => setOrigin(e.target.value)}
              placeholder="例: 東京駅"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              目的地
            </label>
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              placeholder="例: 鎌倉駅"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <button
          onClick={searchRoute}
          disabled={loading}
          className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '検索中...' : 'ルート検索（サンプル）'}
        </button>
      </div>

      {/* 地図表示（サンプル） */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="w-full h-[600px] rounded-lg bg-gradient-to-br from-green-100 to-blue-100 flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4">🗺️</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Google Maps サンプルモード
            </h3>
            <p className="text-gray-600 mb-4">
              実際の地図を表示するには<br />
              Google Maps APIキーの設定が必要です
            </p>
            <div className="bg-white p-4 rounded-lg shadow-sm max-w-sm mx-auto">
              <p className="text-sm text-gray-700">
                📍 ルート検索後、歴史スポットが右側に表示されます
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}