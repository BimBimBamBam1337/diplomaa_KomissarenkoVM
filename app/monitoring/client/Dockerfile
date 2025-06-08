FROM python:3.11-slim

WORKDIR /app

COPY monitoring/client/client.py .
COPY monitoring/client/sys_info.py .

RUN pip install psutil

CMD ["python", "client.py"]
