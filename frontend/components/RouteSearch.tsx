'use client'

import { useState } from 'react'
import { Search, MapPin, Navigation } from 'lucide-react'
import { api } from '@/lib/api'
import { Route, HistoricalSpot } from '@/types'
import toast from 'react-hot-toast'

interface RouteSearchProps {
  onRouteFound: (route: Route) => void
}

export function RouteSearch({ onRouteFound }: RouteSearchProps) {
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!origin || !destination) {
      toast.error('出発地と目的地を入力してください')
      return
    }

    setLoading(true)
    try {
      const response = await api.post('/routes/search', {
        origin,
        destination,
      })

      const routeData = response.data.route
      const spots = response.data.historical_spots

      const savedRouteResponse = await api.post('/routes/save', {
        ...routeData,
        historical_spots: spots,
      })

      onRouteFound(savedRouteResponse.data)
      toast.success('ルートが見つかりました！')
    } catch (error) {
      toast.error('ルートの検索に失敗しました')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 flex items-center">
        <Navigation className="h-5 w-5 mr-2 text-primary-600" />
        ルート検索
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="inline h-4 w-4 mr-1" />
            出発地
          </label>
          <input
            type="text"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            placeholder="例: 東京駅"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="inline h-4 w-4 mr-1" />
            目的地
          </label>
          <input
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="例: 鎌倉駅"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      <button
        onClick={handleSearch}
        disabled={loading}
        className="mt-4 w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {loading ? (
          <span>検索中...</span>
        ) : (
          <>
            <Search className="h-5 w-5 mr-2" />
            ルート検索
          </>
        )}
      </button>
    </div>
  )
}