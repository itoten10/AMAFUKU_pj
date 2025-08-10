export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  total_score: number
  created_at: string
}

export interface Route {
  id: number
  origin: string
  destination: string
  origin_lat: number
  origin_lng: number
  dest_lat: number
  dest_lng: number
  distance: string
  duration: string
  polyline: string
  created_at: string
  historical_spots: HistoricalSpot[]
}

export interface HistoricalSpot {
  id: number
  place_id: string
  name: string
  address?: string
  lat: number
  lng: number
  description?: string
  types?: string[]
}

export interface Quiz {
  id?: number
  spot_id: string
  spot_name: string
  question: string
  options: string[]
  correct_answer: number
  explanation: string
  difficulty: string
  points: number
}

export interface QuizAttempt {
  id: number
  quiz_id: number
  selected_answer: number
  is_correct: boolean
  points_earned: number
  attempted_at: string
}