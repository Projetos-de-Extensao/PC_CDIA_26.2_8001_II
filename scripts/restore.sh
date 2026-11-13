#!/bin/sh
# Restore a backup made by scripts/backup.sh into the running db container.
# Existing tables are dropped and recreated from the dump.
#
# Usage:  sh scripts/restore.sh /home/ubuntu/backups/photomatch_AAAA-MM-DD_HHMM.dump
set -eu
cd "$(dirname "$0")/.."

if [ $# -ne 1 ] || [ ! -s "$1" ]; then
    echo "Usage: $0 <file.dump>" >&2
    exit 1
fi

docker compose exec -T db sh -c 'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists --no-owner' < "$1"
echo "Restored $1"
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "select count(*) || '"' photos'"' from gallery_photo"'
