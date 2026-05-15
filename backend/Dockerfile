FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
VOLUME ["/app/uploads"]
EXPOSE 9000
CMD ["uvicorn", "noti:app", "--host", "0.0.0.0", "--port", "9000"]
