#!/bin/sh
# Update and (re)start PhotoMatch on the EC2:
#   git pull -> docker compose up -d --build -> wait for the healthcheck.
# Migrations and collectstatic run in docker/entrypoint.sh on container start.
#
# Usage (on the EC2, inside the repository):  sh scripts/deploy.sh
set -eu
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
    echo "Missing .env: copy .env.example to .env and fill in the real values." >&2
    exit 1
fi

echo "== git pull"
git pull --ff-only

echo "== docker compose up -d --build"
docker compose up -d --build

echo "== waiting for the web container to be healthy"
attempt=0
while :; do
    status=$(docker inspect --format '{{.State.Health.Status}}' "$(docker compose ps -q web)" 2>/dev/null || echo starting)
    [ "$status" = "healthy" ] && break
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 60 ]; then
        echo "web did not become healthy in 5 minutes. Last logs:" >&2
        docker compose logs --tail 50 web >&2
        exit 1
    fi
    sleep 5
done

docker compose ps
docker image prune -f >/dev/null
echo "Deploy finished: $(git rev-parse --short HEAD)"
