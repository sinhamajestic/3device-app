
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR"

echo "Running database migrations from inside $(pwd)..."
alembic upgrade head

echo "Starting Uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port $PORT

