# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set current working directory
WORKDIR /usr/FraudDetection

# Copy only the requirements.txt initially
COPY requirements.txt /usr/FraudDetection/

# Install the required libraries 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /usr/FraudDetection/

# Expose the port within Docker
EXPOSE 5000

# Use Gunicorn to run the Flask app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]