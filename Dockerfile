# Use official Python 3.10 image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements.txt first (rest will be mounted)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Keep the container open for work
CMD ["/bin/bash"]

