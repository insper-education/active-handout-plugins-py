# Setup based on https://londonappdeveloper.com/django-docker-deployment-with-https-using-letsencrypt/
FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
COPY app/ /app
RUN mkdir -p /app/.static
RUN mkdir -p /app/.media
WORKDIR /app

RUN pip install --upgrade pip
RUN python -m pip install "setuptools==69.5.1" "wheel==0.43.0"
RUN python -m pip install --no-build-isolation "django-allauth==0.43.0"
RUN python -m pip install -r requirements.txt

CMD ["uwsgi", "--socket", ":9000", "--workers", "4", "--master", "--enable-threads", "--module", "active_handout_api.wsgi"]