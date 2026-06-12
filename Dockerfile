FROM python:3.9-slim
WORKDIR /app

RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R flaskuser:flaskuser /app

ENV PATH="/home/flaskuser/.local/bin:${PATH}"

USER flaskuser

EXPOSE 5000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:5000 app:app || sleep 3600"]