FROM python:3.9-slim
WORKDIR /app
RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

COPY --from=builder /root/.local /home/flaskuser/.local
COPY . .

ENV PATH=/home/flaskuser/.local/bin:$PATH
ENV FLASK_ENV=production
USER flaskuser

EXPOSE 5000
CMD ["python", "app.py"]