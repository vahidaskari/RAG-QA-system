FROM python:3.12-bullseye

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.lock

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]