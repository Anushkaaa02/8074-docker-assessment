FROM python:3.9 AS stage1

ARG APP_VERSION=0.1
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

EXPOSE 5000

CMD ["python", "app.py"]

FROM python:3.14.10-slim-trixie AS fixed

ARG APP_VERSION=0.2
ENV APP_VERSION=${APP_VERSION}
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update \
	&& apt-get upgrade -y --no-install-recommends \
	&& pip install --no-cache-dir -r requirements.txt \
	&& useradd --system --create-home --uid 10001 appuser \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

COPY --chown=appuser:appuser app.py ./

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]