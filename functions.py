import json
import os
import hashlib
import sqlite3
import subprocess
import sys
from datetime import datetime


def serialize_pkg(pkg_name, file_path="package_name.ser"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        data = json.load(f)

    if pkg_name not in data:
        data.append(pkg_name)
        with open(file_path, "w") as f:
            json.dump(data, f)
        print(f"Serialized package: {pkg_name}")
    else:
        print(f"Package {pkg_name} is already serialized.")


def hash_pkg_files(pkg_name, db_path="file_hashes.db"):
    try:
        result = subprocess.run(
            ["dpkg", "-L", pkg_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        file_list = result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to get files for package {pkg_name}. {e.stderr.strip()}")
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_hashes (
            file_path TEXT PRIMARY KEY,
            hash TEXT
        )
    """)
    for file_path in file_list:
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                cursor.execute("""
                    INSERT OR REPLACE INTO file_hashes (file_path, hash)
                    VALUES (?, ?)
                """, (file_path, file_hash))
                print(f"Hashed: {file_path}")
            except Exception as e:
                print(f"Error hashing file {file_path}: {e}")

    conn.commit()
    conn.close()


def check_hashes(db_path="file_hashes.db", log_file="discrepancies.log"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path, hash FROM file_hashes")
    records = cursor.fetchall()
    discrepancies = []
    for file_path, stored_hash in records:
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as f:
                    current_hash = hashlib.sha256(f.read()).hexdigest()

                if current_hash != stored_hash:
                    discrepancies.append(file_path)

            except Exception as e:
                with open(log_file, "a") as log:
                    log.write(f"{datetime.now()}: Error reading file {file_path}: {e}\n")
        else:
            with open(log_file, "a") as log:
                log.write(f"{datetime.now()}: File not found: {file_path}\n")

    if discrepancies:
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()}: Discrepancies found in {len(discrepancies)} file(s):\n")
            for file in discrepancies:
                log.write(f"    {file}\n")
    else:
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()}: All files match stored hashes.\n")

    conn.close()


def update_hashes(pkg_name, db_path="file_hashes.db"):
    print(f"Updating hashes for package: {pkg_name}")
    hash_pkg_files(pkg_name, db_path)
    print(f"Hashes updated for package: {pkg_name}")