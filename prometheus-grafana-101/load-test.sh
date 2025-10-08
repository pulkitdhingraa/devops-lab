#!/bin/bash

kubectl port-forward svc/producer 5000:80 &

URL="http://127.0.0.1:5000/submit"

# Infinite load until stopped
while true; do
  # Generate a random payload file
  TASK=$((RANDOM % 1000))
  PAYLOAD="{\"task\": \"process-$TASK\"}"
  echo $PAYLOAD > payload.json

  # Randomize request count & concurrency
  N=$(( (RANDOM % 100) + 200 ))   
  C=$(( (RANDOM % 5) + 5 ))

  echo "Running ab with -n $N -c $C"
  ab -n $N -c $C -p payload.json -T application/json $URL >/dev/null 2>&1

  # Sleep between bursts (random 1–3 sec)
  SLEEP_TIME=$(( (RANDOM % 2) + 1 ))
  echo "Sleeping for $SLEEP_TIME seconds..."
  sleep $SLEEP_TIME
done