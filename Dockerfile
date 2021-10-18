FROM python:3.8

RUN apt-get update

# Set the home directory
ENV HOME /

# Move to the new home dir
WORKDIR /

COPY . .

RUN apt-get -y update
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD python3 server $PORT