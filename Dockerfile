# Use multi-stage build for both Flask and Node apps

# Stage 1: Flask
FROM python:3.9-slim as flask-build

WORKDIR /app

COPY my-flask-app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY my-flask-app/ .

# Stage 2: Node
FROM node:14 as node-build

WORKDIR /app

COPY my-node-app/package*.json ./
RUN npm install

COPY my-node-app/ .

# Stage 3: Combine
FROM python:3.9-slim

WORKDIR /app

# Copy Flask files
COPY --from=flask-build /app /app/my-fl
