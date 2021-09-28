FROM python:3

RUN apt-get update

# Set the home directory
ENV HOME /

# Move to the new home dir
WORKDIR /

COPY . .

EXPOSE 8000

CMD ["python3", "./server.py"]