#!/bin/bash

echo  "Launching the service..."

cat .env.example > .env

cat .env.example_ds > .env.ds

docker-compose up -d

echo  "Service started successfully."

sleep 2