FROM python:3.12-slim

WORKDIR /game_code

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 5000

CMD ["python","game_code.py"] 