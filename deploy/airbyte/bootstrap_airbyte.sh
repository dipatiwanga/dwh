#!/bin/bash
# Booster script for Airbyte

AIRBYTE_DIR="deploy/airbyte"
mkdir -p $AIRBYTE_DIR

echo "Downloading Airbyte setup script..."
curl -L https://github.com/airbytehq/airbyte/raw/master/run-ab-platform.sh -o $AIRBYTE_DIR/run-ab-platform.sh
chmod +x $AIRBYTE_DIR/run-ab-platform.sh

echo "Airbyte setup script is ready at $AIRBYTE_DIR/run-ab-platform.sh"
echo "To start Airbyte, run: ./$AIRBYTE_DIR/run-ab-platform.sh"
