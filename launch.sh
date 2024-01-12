#!/bin/bash

# Setup
function setup() {
    echo "Setting up the environment..."
    pip install -r requirements.txt
}

# Run
function run() {
    echo "Running the Python script..."
    python.exe gui.py
}

# Clean-up
function clean_up() {
    echo "Cleaning up resources..."
}

# Main execution
if [ "$1" == "setup" ]; then
    setup
elif [ "$1" == "run" ]; then
    setup
    run
elif [ "$1" == "clean-up" ]; then
    clean_up
else
    echo "Usage: $0 {setup|run|clean-up}"
    exit 1
fi
