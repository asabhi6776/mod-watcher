FROM python:3.14.0b4-alpine
LABEL maintainer="github.com/asabhi6776"

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    && pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app