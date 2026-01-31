#!/bin/bash
echo "🚀 Starting ShopMind AI..."

# Start Backend
echo "Starting Backend (FastAPI)..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start Frontend
echo "Starting Frontend (Next.js)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ ShopMind is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"

# Kill both on exit
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
