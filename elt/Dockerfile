FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client-15 cron

COPY start.sh /app/stat.sh
COPY elt_script.py .

WORKDIR /app

RUN echo "0 19 * * * postgres timeout 30s python /app/elt_script.py" | crontab - 
#runs script at 19:00 everyday

CMD ["python", "elt_script.py"]
