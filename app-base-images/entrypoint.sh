#!/bin/sh
if [ ! -f /app/stratus_init.sh ]; then
  echo "Error: /app/stratus_init.sh not found!"
  exit 1
fi

chmod +x /app/stratus_init.sh
exec /app/stratus_init.sh