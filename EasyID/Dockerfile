# Base Image
FROM python:3.7

# Create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# Install system dependencies
RUN apt-get update
RUN python -m pip install -r requirements.txt

EXPOSE 8000
CMD daphne -b 0.0.0.0 -p 8000 EasyID.asgi:application