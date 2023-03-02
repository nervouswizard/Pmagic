#!/bin/bash

# Define the name of the virtual environment
venv_name="venvPmagic"

# Create a new virtual environment
python -m venv $venv_name

# Activate the virtual environment
source $venv_name/Scripts/activate

# Install the required packages
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate