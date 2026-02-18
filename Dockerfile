FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

ARG ENVIRONMENT=production

COPY requirements/ ./requirements/

RUN pip install --upgrade pip --root-user-action=ignore && \
    if [ "$ENVIRONMENT" = "development" ]; then \
        pip install --root-user-action=ignore -r requirements/development.txt; \
    else \
        pip install --root-user-action=ignore -r requirements/production.txt; \
    fi

COPY entrypoint.sh .
COPY strava_stats/ ./strava_stats/
COPY activities/ ./activities/
COPY templates/ ./templates/
COPY manage.py .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
