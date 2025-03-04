FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3.9 python3-pip
RUN ln -s /usr/bin/python3.9 /usr/bin/python

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"] 