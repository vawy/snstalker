# === STAGE 1: Builder ===
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml uv.lock requirements.txt ./
RUN uv venv /app/.venv && uv pip install --no-cache-dir -r requirements.txt

# === STAGE 2: Runtime ===
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app
COPY --from=builder --chown=app:app /app/.venv /home/app/.venv
ENV PATH=/home/app/.venv/bin:$PATH
ENV PYTHONPATH=/home/app/.venv/lib/python3.11/site-packages:$PYTHONPATH
COPY --chown=app:app . .
EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "snstalker_project.wsgi:application"]
CMD ["uvicorn", "snstalker_project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
