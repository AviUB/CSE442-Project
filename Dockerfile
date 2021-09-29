FROM python:3.8

ENV HOME /root

WORKDIR /root

COPY . .

RUN apt-get -y update
RUN pip install -r requirements.txt

EXPOSE $PORT

python3 ./sample_site/server.py $PORT