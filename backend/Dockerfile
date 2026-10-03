FROM node:22-alpine AS ui
WORKDIR /ui
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend ./
RUN npm run build

FROM python:3.13-slim-trixie

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 1000 --home-dir /app --shell /usr/sbin/nologin susiturkki \
    && mkdir -p /data \
    && chown susiturkki:susiturkki /data

WORKDIR /app
COPY backend/pyproject.toml .
COPY backend/src src
COPY --from=ui /ui/dist /app/static
RUN pip install --no-cache-dir .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/data/susiturkki.db \
    UI_DIR=/app/static
USER susiturkki
CMD ["python", "-m", "susiturkki.infrastructure.serve"]
