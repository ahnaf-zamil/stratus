#!/bin/sh
if [ ! -f /app/stratus_init.sh ]; then
  echo "Error: /app/stratus_init.sh not found!"
  exit 1
fi

# These variables are passed in when the container is created
echo "Running deployment $DEPLOYMENT_ID. Container ID: $LOGICAL_CONTAINER_ID" 

chmod +x /app/stratus_init.sh
exec /app/stratus_init.sh