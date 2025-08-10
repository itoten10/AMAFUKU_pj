'use client'

import { useAuthStore } from '@/store/auth'
import { Car, LogOut, User } from 'lucide-react'

export function Header() {
  const { user, logout } = useAuthStore()

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <Car className="h-8 w-8 text-primary-600" />
            <h1 className="text-xl font-bold text-gray-900">
              Famoly Drive
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <User className="h-5 w-5 text-gray-600" />
              <span className="text-gray-700">{user?.username}</span>
              <span className="font-semibold text-primary-600">
                {user?.total_score}点
              </span>
            </div>

            <button
              onClick={logout}
              className="flex items-center space-x-1 text-gray-600 hover:text-gray-900"
            >
              <LogOut className="h-5 w-5" />
              <span>ログアウト</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}