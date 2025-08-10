'use client'

import { useEffect, useState } from 'react'
import { Trophy, TrendingUp } from 'lucide-react'
import { api } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

interface RankingUser {
  id: number
  username: string
  total_score: number
}

export function ScoreBoard() {
  const { user } = useAuthStore()
  const [ranking, setRanking] = useState<RankingUser[]>([])

  useEffect(() => {
    fetchRanking()
  }, [])

  const fetchRanking = async () => {
    try {
      const response = await api.get('/users/ranking')
      setRanking(response.data)
    } catch (error) {
      console.error('Failed to fetch ranking:', error)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 flex items-center">
        <Trophy className="h-5 w-5 mr-2 text-yellow-500" />
        ランキング
      </h2>

      <div className="mb-6 p-4 bg-primary-50 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">あなたのスコア</span>
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5 text-primary-600" />
            <span className="text-2xl font-bold text-primary-600">
              {user?.total_score || 0}点
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        {ranking.map((player, index) => (
          <div
            key={player.id}
            className={`flex items-center justify-between p-3 rounded-lg ${
              player.id === user?.id
                ? 'bg-primary-100 border border-primary-300'
                : 'bg-gray-50'
            }`}
          >
            <div className="flex items-center space-x-3">
              <span
                className={`text-lg font-semibold ${
                  index === 0
                    ? 'text-yellow-500'
                    : index === 1
                    ? 'text-gray-400'
                    : index === 2
                    ? 'text-orange-600'
                    : 'text-gray-600'
                }`}
              >
                {index + 1}位
              </span>
              <span className="font-medium">
                {player.username}
                {player.id === user?.id && ' (あなた)'}
              </span>
            </div>
            <span className="font-semibold">{player.total_score}点</span>
          </div>
        ))}
      </div>
    </div>
  )
}