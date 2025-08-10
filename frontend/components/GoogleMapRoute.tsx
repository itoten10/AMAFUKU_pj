'use client'

import { useState, useCallback, useRef, useEffect } from 'react'
import { Loader } from '@googlemaps/js-api-loader'
import toast from 'react-hot-toast'

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

interface GoogleMapRouteProps {
  onRouteFound: (routeInfo: RouteInfo) => void
  onSpotsFound: (spots: HistoricalSpot[]) => void
}

export function GoogleMapRoute({ onRouteFound, onSpotsFound }: GoogleMapRouteProps) {
  const [origin, setOrigin] = useState('東京駅')
  const [destination, setDestination] = useState('鎌倉駅')
  const [loading, setLoading] = useState(false)
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<google.maps.Map | null>(null)
  const directionsServiceRef = useRef<google.maps.DirectionsService | null>(null)
  const directionsRendererRef = useRef<google.maps.DirectionsRenderer | null>(null)
  const placesServiceRef = useRef<google.maps.places.PlacesService | null>(null)

  const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY

  useEffect(() => {
    if (!GOOGLE_MAPS_API_KEY) {
      console.error('Google Maps API key not found')
      return
    }

    const loader = new Loader({
      apiKey: GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['places', 'geometry']
    })

    loader.load().then(() => {
      if (!mapRef.current) return

      // 地図を初期化
      const map = new google.maps.Map(mapRef.current, {
        center: { lat: 35.6812, lng: 139.7671 }, // 東京駅
        zoom: 10
      })

      mapInstanceRef.current = map
      directionsServiceRef.current = new google.maps.DirectionsService()
      directionsRendererRef.current = new google.maps.DirectionsRenderer()
      placesServiceRef.current = new google.maps.places.PlacesService(map)

      directionsRendererRef.current.setMap(map)
    }).catch((error) => {
      console.error('Google Maps API loading error:', error)
      toast.error('Google Maps の読み込みに失敗しました')
    })
  }, [GOOGLE_MAPS_API_KEY])

  const searchRoute = useCallback(async () => {
    if (!directionsServiceRef.current || !directionsRendererRef.current || !mapInstanceRef.current) {
      toast.error('地図が初期化されていません')
      return
    }

    if (!origin.trim() || !destination.trim()) {
      toast.error('出発地と目的地を入力してください')
      return
    }

    setLoading(true)

    try {
      const request: google.maps.DirectionsRequest = {
        origin,
        destination,
        travelMode: google.maps.TravelMode.DRIVING,
        language: 'ja'
      }

      const result = await new Promise<google.maps.DirectionsResult>((resolve, reject) => {
        directionsServiceRef.current!.route(request, (result, status) => {
          if (status === google.maps.DirectionsStatus.OK && result) {
            resolve(result)
          } else {
            reject(new Error(`ルート検索に失敗しました: ${status}`))
          }
        })
      })

      // ルートを地図に表示
      directionsRendererRef.current.setDirections(result)

      const route = result.routes[0]
      const leg = route.legs[0]

      const routeInfo: RouteInfo = {
        origin,
        destination,
        distance: leg.distance?.text || '不明',
        duration: leg.duration?.text || '不明',
        route
      }

      onRouteFound(routeInfo)

      // ルート周辺の歴史スポットを検索
      await searchHistoricalSpots(route)

      toast.success('ルートが見つかりました！')
    } catch (error) {
      console.error('Route search error:', error)
      toast.error('ルート検索に失敗しました')
    } finally {
      setLoading(false)
    }
  }, [origin, destination, onRouteFound, onSpotsFound])

  const searchHistoricalSpots = async (route: google.maps.DirectionsRoute) => {
    if (!placesServiceRef.current || !mapInstanceRef.current) return

    try {
      const path = route.overview_path
      const samplePoints = []
      
      // ルート上の点をサンプリング
      const interval = Math.max(1, Math.floor(path.length / 5))
      for (let i = 0; i < path.length; i += interval) {
        samplePoints.push(path[i])
        if (samplePoints.length >= 5) break
      }

      const historicalSpots: HistoricalSpot[] = []
      const processedPlaceIds = new Set<string>()
      const keywords = ['神社', '寺', '城', '史跡', '博物館']

      for (let i = 0; i < samplePoints.length; i++) {
        const point = samplePoints[i]
        const keyword = keywords[i % keywords.length]

        try {
          const request: google.maps.places.PlaceSearchRequest = {
            location: point,
            radius: 3000,
            keyword,
            language: 'ja'
          }

          const places = await new Promise<google.maps.places.PlaceResult[]>((resolve, reject) => {
            placesServiceRef.current!.nearbySearch(request, (results, status) => {
              if (status === google.maps.places.PlacesServiceStatus.OK && results) {
                resolve(results)
              } else {
                resolve([])
              }
            })
          })

          for (const place of places.slice(0, 2)) {
            if (place.place_id && !processedPlaceIds.has(place.place_id)) {
              processedPlaceIds.add(place.place_id)

              const spot: HistoricalSpot = {
                place_id: place.place_id,
                name: place.name || '不明な場所',
                address: place.vicinity || '',
                lat: place.geometry?.location?.lat() || 0,
                lng: place.geometry?.location?.lng() || 0,
                description: generateDescription(place.name || '')
              }

              historicalSpots.push(spot)

              // 地図にマーカーを追加
              const marker = new google.maps.Marker({
                position: { lat: spot.lat, lng: spot.lng },
                map: mapInstanceRef.current,
                title: spot.name,
                icon: {
                  url: 'https://maps.google.com/mapfiles/ms/icons/orange-dot.png'
                }
              })

              // 情報ウィンドウを追加
              const infoWindow = new google.maps.InfoWindow({
                content: `
                  <div style="max-width: 200px;">
                    <h3 style="margin: 0 0 8px 0; font-size: 14px; font-weight: bold;">${spot.name}</h3>
                    <p style="margin: 0 0 8px 0; font-size: 12px; color: #666;">${spot.address}</p>
                    <p style="margin: 0; font-size: 12px;">${spot.description}</p>
                  </div>
                `
              })

              marker.addListener('click', () => {
                infoWindow.open(mapInstanceRef.current, marker)
              })

              if (historicalSpots.length >= 5) break
            }
          }

          if (historicalSpots.length >= 5) break
        } catch (error) {
          console.error('Places search error:', error)
        }
      }

      if (historicalSpots.length === 0) {
        // サンプルデータを追加
        historicalSpots.push(
          {
            place_id: 'sample_1',
            name: '鎌倉大仏',
            address: '神奈川県鎌倉市長谷',
            lat: 35.3169,
            lng: 139.5359,
            description: '鎌倉大仏は13世紀に建立された国宝の仏像です。'
          },
          {
            place_id: 'sample_2',
            name: '鶴岡八幡宮',
            address: '神奈川県鎌倉市雪ノ下',
            lat: 35.3249,
            lng: 139.5565,
            description: '鶴岡八幡宮は鎌倉の守護神として古くから信仰されています。'
          }
        )
      }

      onSpotsFound(historicalSpots)
    } catch (error) {
      console.error('Historical spots search error:', error)
    }
  }

  const generateDescription = (name: string): string => {
    const descriptions: { [key: string]: string } = {
      "神社": `${name}は地域の守り神として古くから信仰されている神社です。`,
      "寺": `${name}は歴史ある寺院で、多くの参拝者が訪れます。`,
      "城": `${name}は戦国時代の歴史を今に伝える貴重な史跡です。`,
      "博物館": `${name}では地域の歴史や文化について学ぶことができます。`,
    }

    for (const [key, desc] of Object.entries(descriptions)) {
      if (name.includes(key)) {
        return desc
      }
    }

    return `${name}は歴史的に重要な場所として知られています。`
  }

  if (!GOOGLE_MAPS_API_KEY) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-red-600">
          <p>Google Maps API キーが設定されていません</p>
          <p className="text-sm">.env.local ファイルを確認してください</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* ルート検索フォーム */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">ルート検索</h2>
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
          {loading ? '検索中...' : 'ルート検索'}
        </button>
      </div>

      {/* 地図表示 */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div 
          ref={mapRef} 
          className="w-full h-[600px] rounded-lg"
          style={{ minHeight: '600px' }}
        />
      </div>
    </div>
  )
}