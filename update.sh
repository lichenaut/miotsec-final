#!/bin/bash

SER_FILE="package_name.ser"

if [ ! -f "$SER_FILE" ]; then
    exit 0
fi

DB_PATH="file_hashes.db"

PACKAGE_NAME=$(cat "$SER_FILE")

python3 -c "from functions import update_hashes; update_hashes('$PACKAGE_NAME', db_path='$DB_PATH')"

echo "$(date): Hashes updated for package '$PACKAGE_NAME' after apt upgrade."
