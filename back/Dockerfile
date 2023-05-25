FROM python:3.11
WORKDIR /app
ADD . /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "/app/entrypoint.sh"]