#!/bin/bash

# Function for setup
setup_project() {
  # Check if the venv directory exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    else
        echo "Virtual environment already exists."
    fi

    source ./venv/bin/activate
    pip install -r requirements.txt

    # Check for .env file and create if not exists
    if [[ ! -f ".env" ]]; then
        echo ".env file not found. Creating one."

        # Prompt for user input
        read -p "Enter Username: " username
        read -p "Enter Password: " password
        read -p "Enter Domoticz IP Address: " domoticz_ip
        read -p "Enter Domoticz Port: " domoticz_port

        # Create .env file with grouped echo commands
        {
            echo "USERNAME=$username"
            echo "PASSWORD=$password"
            echo "DOMOTICZ_IP=$domoticz_ip"
            echo "DOMOTICZ_PORT=$domoticz_port"
        } > .env

        echo ".env file created."
    fi
}

# Function for running the application
run_project() {
    source ./venv/bin/activate
    python main.py
}

# Check the provided argument and act accordingly
case "$1" in
    --setup)
        setup_project
        ;;
    --run)
        run_project
        ;;
    *)
        echo "Usage: $0 [--setup | --run]"
        exit 1
        ;;
esac