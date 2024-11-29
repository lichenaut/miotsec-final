#!/bin/bash

# This script is intended to be run by a cron job.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="$SCRIPT_DIR/file_hashes.db"

python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from functions import check_hashes; check_hashes(db_path='$DB_PATH')"

echo "$(date): Hash check completed."
