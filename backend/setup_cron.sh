#!/bin/bash

# Setup cron job to cleanup resolved reports every 5 minutes
# This script should be run as root or with appropriate permissions

# Get the current directory (backend directory)
BACKEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$(which python3)"

# Create the cron job entry
CRON_JOB="*/5 * * * * cd $BACKEND_DIR && $PYTHON_PATH cleanup_script.py >> /var/log/disaster_cleanup.log 2>&1"

# Add the cron job (this will add it to the current user's crontab)
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Cron job added successfully!"
echo "The cleanup script will run every 5 minutes."
echo "Logs will be written to /var/log/disaster_cleanup.log"
echo ""
echo "To view the cron job: crontab -l"
echo "To remove the cron job: crontab -e (then delete the line)"
echo ""
echo "To test the cleanup manually:"
echo "  cd $BACKEND_DIR"
echo "  $PYTHON_PATH cleanup_script.py"
