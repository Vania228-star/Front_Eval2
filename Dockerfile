FROM python:3.9-slim

WORKDIR /app

RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

RUN chown -r flaskuser:flaskuser /app

ENV PATH=/home/flaskuser/.local/bin:$PATH
ENV FLASK_ENV=production

USER flaskuser

EXPOSE 5000
CMD ["python", "app.py"]