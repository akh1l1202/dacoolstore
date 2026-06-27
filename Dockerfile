# Use a slim official Python base image
FROM python:3.9-slim

# Install system dependencies needed for Tkinter (underlying engine for PySimpleGUI)
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set default command to run the package
CMD ["python", "-m", "dacoolstore"]
