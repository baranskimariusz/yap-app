FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++6 \
    libgomp1 \
    cron \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/app/llama.cpp/build/ggml/src:/app/llama.cpp/build/src

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh
RUN chmod +x /app/scraper-cron.sh

CMD ["./entrypoint.sh", "./scraper-cron.sh"]