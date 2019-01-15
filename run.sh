#!/bin/bash

export LOG_LEVEL=INFO
export WTBO_KAFKA_URL="localhost:9092"
export WTBO_SLEEP_MS=60000
set -e
python3 src
