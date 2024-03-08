FROM python:3.11.8-slim-bookworm

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]