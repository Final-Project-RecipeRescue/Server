FROM ubuntu:latest
LABEL authors="nissa"

ENTRYPOINT ["top", "-b"]

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update

EXPOSE 8000

ENV SPOONACULAR_API_KEY 1965ed333db7456597d4a9e1f10d35f7
ENV MONGO_USER admin
ENV MONGO_PASS secret123
ENV FIREBASE_KEY_ID 9d8c8a63421445a506c5655d5a32250319584ed7
ENV databaseURL "https://reciperescue-6da9c-default-rtdb.europe-west1.firebasedatabase.app"
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]