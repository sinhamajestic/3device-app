
set -e
echo "Running database migrations..."
alembic -c backend/alembic.ini upgrade head

echo "Starting Uvicorn server..."
uvicorn backend.main:app --host 0.0.0.0 --port $PORT

