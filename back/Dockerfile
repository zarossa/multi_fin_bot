FROM python:3.11
WORKDIR /app
ADD . /app
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py migrate --no-input
CMD gunicorn proj.wsgi:application --bind 0.0.0.0:8000