#!/bin/bash

# Step 1: Force remove the 'NeuroRecon' directory
echo "Removing the 'NeuroRecon' directory"
rm -rf NeuroRecon
if [ $? -ne 0 ]; then
    echo "Failed to remove 'NeuroRecon'. Exiting."
    exit 1
fi

# Step 2: Clone the repository from GitHub
echo "Cloning the NeuroRecon repository from GitHub"
git clone https://github.com/bigdatanotesbyarun/NeuroRecon.git
if [ $? -ne 0 ]; then
    echo "Failed to clone the repository. Exiting."
    exit 1
fi

# Step 3: Change to the 'NeuroRecon' directory
echo "Changing directory to 'NeuroRecon'"
cd NeuroRecon
if [ $? -ne 0 ]; then
    echo "Failed to change directory to 'NeuroRecon'. Exiting."
    exit 1
fi

# Step 4: Activate the Python virtual environment
echo "Activating virtual environment"
source /home/ubuntu/NeuroReconEnv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate the virtual environment. Exiting."
    exit 1
fi

# Step 5: Set the environment variable for production
echo "Setting environment file for production"
export ENV_FILE=prod.env
if [ $? -ne 0 ]; then
    echo "Failed to set the environment variable. Exiting."
    exit 1
fi

# Step 6: Start the Django development server
echo "Starting Django server at 0.0.0.0:8000"
python manage.py runserver 0.0.0.0:8000
if [ $? -ne 0 ]; then
    echo "Failed to start the Django server. Exiting."
    exit 1
fi

echo "All commands executed successfully!"
