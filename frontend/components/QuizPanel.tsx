'use client'

import { useState } from 'react'
import { BookOpen, Check, X, AlertCircle } from 'lucide-react'
import { api } from '@/lib/api'
import { HistoricalSpot, Quiz } from '@/types'
import toast from 'react-hot-toast'
import { useAuthStore } from '@/store/auth'

interface QuizPanelProps {
  spot: HistoricalSpot
  routeId?: number
}

export function QuizPanel({ spot, routeId }: QuizPanelProps) {
  const { fetchUser } = useAuthStore()
  const [quiz, setQuiz] = useState<Quiz | null>(null)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [isAnswered, setIsAnswered] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(false)
  const [difficulty, setDifficulty] = useState('中学生')

  const generateQuiz = async () => {
    setLoading(true)
    try {
      const response = await api.post('/quizzes/generate', {
        place_id: spot.place_id,
        name: spot.name,
        address: spot.address,
        lat: spot.lat,
        lng: spot.lng,
        types: spot.types,
        description: spot.description,
      }, {
        params: { difficulty }
      })

      setQuiz(response.data)
      setSelectedAnswer(null)
      setIsAnswered(false)
      setIsCorrect(false)
    } catch (error) {
      toast.error('クイズの生成に失敗しました')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const submitAnswer = async () => {
    if (selectedAnswer === null || !quiz) return

    try {
      // Save quiz if it doesn't have an ID
      let quizId = quiz.id
      if (!quizId) {
        const saveResponse = await api.post('/quizzes/save', quiz)
        quizId = saveResponse.data.id
      }

      // Submit attempt
      const response = await api.post('/quizzes/attempt', {
        quiz_id: quizId,
        route_id: routeId,
        selected_answer: selectedAnswer,
      })

      setIsAnswered(true)
      setIsCorrect(response.data.is_correct)

      if (response.data.is_correct) {
        toast.success(`正解！ +${response.data.points_earned}ポイント`)
        await fetchUser() // Update user score
      } else {
        toast.error('不正解... もう一度考えてみよう！')
      }
    } catch (error) {
      toast.error('回答の送信に失敗しました')
      console.error(error)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 flex items-center">
        <BookOpen className="h-5 w-5 mr-2 text-primary-600" />
        {spot.name}のクイズ
      </h2>

      {!quiz ? (
        <div className="space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-2">{spot.description}</p>
            <p className="text-xs text-gray-500">{spot.address}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              難易度を選択
            </label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="小学生">小学生</option>
              <option value="中学生">中学生</option>
              <option value="高校生">高校生</option>
            </select>
          </div>

          <button
            onClick={generateQuiz}
            disabled={loading}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition disabled:opacity-50"
          >
            {loading ? 'クイズを生成中...' : 'クイズに挑戦！'}
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="font-medium text-gray-900">{quiz.question}</p>
          </div>

          <div className="space-y-2">
            {quiz.options.map((option, index) => (
              <button
                key={index}
                onClick={() => !isAnswered && setSelectedAnswer(index)}
                disabled={isAnswered}
                className={`w-full text-left p-3 rounded-lg border-2 transition ${
                  isAnswered
                    ? index === quiz.correct_answer
                      ? 'border-green-500 bg-green-50'
                      : index === selectedAnswer && !isCorrect
                      ? 'border-red-500 bg-red-50'
                      : 'border-gray-200 bg-gray-50'
                    : selectedAnswer === index
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                } ${isAnswered ? 'cursor-not-allowed' : 'cursor-pointer'}`}
              >
                <div className="flex items-center justify-between">
                  <span>{option}</span>
                  {isAnswered && index === quiz.correct_answer && (
                    <Check className="h-5 w-5 text-green-600" />
                  )}
                  {isAnswered && index === selectedAnswer && !isCorrect && (
                    <X className="h-5 w-5 text-red-600" />
                  )}
                </div>
              </button>
            ))}
          </div>

          {isAnswered && (
            <div className={`p-4 rounded-lg ${
              isCorrect ? 'bg-green-50 border border-green-200' : 'bg-yellow-50 border border-yellow-200'
            }`}>
              <div className="flex items-start space-x-2">
                <AlertCircle className={`h-5 w-5 mt-0.5 ${
                  isCorrect ? 'text-green-600' : 'text-yellow-600'
                }`} />
                <div>
                  <p className={`font-medium ${
                    isCorrect ? 'text-green-800' : 'text-yellow-800'
                  }`}>
                    {isCorrect ? '正解です！' : 'もう一度考えてみましょう'}
                  </p>
                  <p className="text-sm text-gray-700 mt-1">
                    {quiz.explanation}
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="flex space-x-3">
            {!isAnswered ? (
              <button
                onClick={submitAnswer}
                disabled={selectedAnswer === null}
                className="flex-1 bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                回答する
              </button>
            ) : (
              <button
                onClick={generateQuiz}
                className="flex-1 bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition"
              >
                新しいクイズ
              </button>
            )}
            
            <button
              onClick={() => {
                setQuiz(null)
                setSelectedAnswer(null)
                setIsAnswered(false)
              }}
              className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition"
            >
              閉じる
            </button>
          </div>
        </div>
      )}
    </div>
  )
}