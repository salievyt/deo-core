FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home --uid 10001 app
COPY --chown=app:app . .
RUN mkdir -p /app/media /app/private_uploads /app/staticfiles /app/.cache && chown -R app:app /app
USER app
EXPOSE 8000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
