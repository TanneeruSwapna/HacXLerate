#!/bin/bash

echo "========================================"
echo "  B2B Marketplace Application Startup"
echo "========================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org/"
    exit 1
fi

echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo
echo "Starting all services..."
echo "This may take a few minutes for first-time setup..."
echo

python3 run_all_services.py --install

echo
echo "Press Enter to exit..."
read
