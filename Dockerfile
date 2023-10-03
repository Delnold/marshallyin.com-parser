FROM python:3.8
LABEL authors="Delnold"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "run-spider.py"]