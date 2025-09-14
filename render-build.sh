set -e

echo "Changing directory to /backend..."
cd backend

echo "Running migrations from inside $(pwd)..."
alembic upgrade head

echo "Starting server..."
uvicorn main:app --host 0.0.0.0 --port $PORT
