FROM python:3.9-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 gcc libpq-dev python3-dev \
    zlib1g-dev libjpeg-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
COPY start.sh .

RUN chmod +x start.sh

CMD ["sh", "./start.sh"]

EXPOSE 8000
EXPOSE 8001