FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 1000 --home-dir /app --shell /usr/sbin/nologin susiturkki \
    && mkdir -p /data \
    && chown susiturkki:susiturkki /data

WORKDIR /app
COPY pyproject.toml .
COPY src src
RUN pip install --no-cache-dir .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/data/susiturkki.db
EXPOSE 8000
USER susiturkki
CMD ["uvicorn", "susiturkki.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
