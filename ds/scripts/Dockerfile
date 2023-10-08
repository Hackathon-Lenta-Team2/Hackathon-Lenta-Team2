FROM python:3.10

WORKDIR app

COPY requirements.txt .

RUN apt-get update && apt-get install
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR src

CMD ["python", "app.py"]