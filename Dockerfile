FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
COPY ./task2/knowledge_base/ /app/knowledge_base/
COPY ./task3/build_index.py /app/build_index.py
COPY ./task7/evaluate.py /app/evalute.py
COPY ./task7/golden_questions.json /app/golden_questions.json


RUN python build_index.py

RUN rm -rf /app/knowledge_base

CMD ["python", "bot.py"]