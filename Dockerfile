# syntax=docker/dockerfile:1

# ---- Build stage: compile wheels (dlib takes several minutes) -------------
FROM python:3.12-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- Runtime stage --------------------------------------------------------
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends libopenblas0 liblapack3 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 app
WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*.whl && rm -rf /wheels
COPY --chown=app:app . .
RUN chmod +x docker/entrypoint.sh && mkdir -p staticfiles && chown app:app /app staticfiles
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=4)"
ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn", "photomatch.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
