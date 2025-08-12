#!/bin/bash

echo "Starting Famoly Drive Servers..."
echo ""

# Backend APIサーバーを起動
echo "[1/2] Starting Backend API Server (Port 8000)..."
cd backend
uvicorn simple_api:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

sleep 3

# Frontendサーバーを起動
echo "[2/2] Starting Frontend Server (Port 3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "===================================="
echo "Servers are running!"
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend:    http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "===================================="

# 終了時にすべてのプロセスを停止
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

# サーバーを実行し続ける
wait