FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 80

CMD ["./entrypoint.sh"]

# docker build -t resource-lock-test .
# docker run --rm resource-lock-test