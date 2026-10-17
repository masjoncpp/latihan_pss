FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
FROM ... AS builder
# build/install artifacts

FROM ... AS runtime
# copy only required runtime artifacts
# run application
