FROM python:3.10-alpine

EXPOSE 8000

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
