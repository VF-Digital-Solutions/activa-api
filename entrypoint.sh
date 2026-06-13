#!/bin/sh
set -e

echo "Waiting for database..."
until python -c "
import os, sys
import MySQLdb
try:
    MySQLdb.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'hometrack'),
        passwd=os.environ.get('DB_PASSWORD', 'hometrack'),
        db=os.environ.get('DB_NAME', 'hometrack_dev'),
        port=int(os.environ.get('DB_PORT', '3306'))
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    echo "  database not ready, retrying in 2s..."
    sleep 2
done

echo "Database ready."
exec "$@"
