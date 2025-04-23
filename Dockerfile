# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the files into the container
COPY . .

# Install required packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for Jupyter
EXPOSE 8888

CMD ["tail", "-f", "/dev/null"]
