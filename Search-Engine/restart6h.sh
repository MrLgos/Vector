#!/bin/bash

while true; do
  # Check if process main.py exists
  if pgrep -f "python3 main.py" >/dev/null; then
    echo "Existing process found. Terminating..."
    pkill -f "python3 main.py"  # kill the process
  else
    echo "No existing process found."
  fi

  echo "Starting main.py..."
  nohup python3 main.py > /dev/null 2>&1 &  # run the process again

  sleep 6h  # Wait for 6 hours
done

