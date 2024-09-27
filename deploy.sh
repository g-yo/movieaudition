#!/bin/bash

# Navigate to the project directory
cd /home/ec2-user/auditions

# Activate virtual environment if you have one, else skip this step
# source venv/bin/activate

# Pull the latest changes from the repository
git pull origin main

# Install any new dependencies
pip3 install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Apply any new migrations
python3 manage.py migrate

# Restart Gunicorn
sudo systemctl restart gunicorn
