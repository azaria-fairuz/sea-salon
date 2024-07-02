# base images
FROM python:3.11-slim

# Install PostgreSQL development libraries
RUN apt-get update && \
    apt-get install -y \
    curl \ 
    libpq-dev \
    gcc && \
    apt-get clean

# Create the directory for the root certificate
RUN mkdir -p /root/.postgresql

# Download the root certificate
RUN curl -o /root/.postgresql/root.crt https://cockroachlabs.cloud/clusters/10bfb27b-c589-4634-a372-5895f36ade2c/cert

# workdir is used to set the pwd inside docker container
WORKDIR /code
COPY requirements.txt /requirements.txt

# Install pip dependancy.
RUN pip install -r /requirements.txt

# copy whole directory inside /code working directory.
COPY . /code

# This command execute at the time when conatiner start.

CMD ["python3", "__init__.py"]