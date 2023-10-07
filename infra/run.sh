#!/bin/bash

cat .env.example > .env

cat .env.example_ds > .env.ds

docker-compose up -d