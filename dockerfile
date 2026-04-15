# Stage 1 — builder
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 — runner
FROM python:3.12-slim
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

# Non-root user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home --shell /bin/false appuser && \
    chown -R appuser:appgroup /app
USER appuser

ENV PORT=8000
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--chdir", "src", "app:app"]
