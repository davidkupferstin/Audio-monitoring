FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app
COPY services/meta_flow /app/services/meta_flow
COPY shared /app/shared

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/shared

CMD ["python", "-m", "services.meta_flow.main"]