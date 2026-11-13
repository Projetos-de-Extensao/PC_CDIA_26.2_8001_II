#!/bin/sh
# Back up the PhotoMatch database with pg_dump (custom format, compressed).
#
# Usage:  sh scripts/backup.sh
# Env:    BACKUP_DIR     (default: $HOME/backups)
#         KEEP_DAYS      (default: 7)  local dumps older than this are deleted
#         BACKUP_S3_URI  (optional, e.g. s3://my-bucket/backups/) copy off the instance;
#                        needs the AWS CLI and an instance role with s3:PutObject
# Cron:   0 3 * * * cd /home/ubuntu/PC_CDIA_26.2_8001_II && sh scripts/backup.sh >> /home/ubuntu/backup.log 2>&1
set -eu
cd "$(dirname "$0")/.."

BACKUP_DIR="${BACKUP_DIR:-$HOME/backups}"
KEEP_DAYS="${KEEP_DAYS:-7}"
mkdir -p "$BACKUP_DIR"

file="$BACKUP_DIR/photomatch_$(date +%F_%H%M).dump"
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$file"

if [ ! -s "$file" ]; then
    echo "Backup is empty: $file" >&2
    exit 1
fi
echo "Backup written: $file ($(du -h "$file" | cut -f1))"

if [ -n "${BACKUP_S3_URI:-}" ]; then
    aws s3 cp "$file" "$BACKUP_S3_URI"
fi

find "$BACKUP_DIR" -name 'photomatch_*.dump' -mtime +"$KEEP_DAYS" -delete
