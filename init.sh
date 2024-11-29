#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <package_name>"
    exit 1
fi

PACKAGE_NAME=$1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from functions import serialize_pkg; serialize_pkg('$PACKAGE_NAME')"
python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from functions import hash_pkg_files; hash_pkg_files('$PACKAGE_NAME')"

echo "Monitoring initialized for package: $PACKAGE_NAME"
