FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir

COPY . .

CMD ["python", "main.py"]