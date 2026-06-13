# ── base: dependencias del sistema + paquetes Python ─────────────────────────
FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── development: código montado como volumen, runserver ───────────────────────
FROM base AS development

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY . .
ENV DJANGO_SETTINGS_MODULE=config.settings.development
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ── production: gunicorn, sin volúmenes, ajustes de rendimiento ───────────────
FROM base AS production

RUN pip install --no-cache-dir gunicorn==23.0.0

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY . .
ENV DJANGO_SETTINGS_MODULE=config.settings.production
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
