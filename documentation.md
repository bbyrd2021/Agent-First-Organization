# Setting Up a Python 3.10 Development Environment with Docker

This guide explains how to set up a Python 3.10 development environment using Docker. The setup ensures that dependencies are installed and that your project directory is mounted, allowing you to work on your code without modifying your local Python installation.

1. Prerequisites

Ensure you have the following installed on your system:

Docker Desktop

Basic command-line knowledge

2. Project Directory Structure

Ensure your project is located in the following directory:

/Users/brandonbyrd/AgentFirst/Agent-First-Organization/

This directory will be mounted inside the Docker container.

3. Create a Dockerfile

Inside your project directory (Agent-First-Organization), create a file named Dockerfile and add the following content:

# Use official Python 3.10 image

FROM python:3.10

# Set the working directory inside the container

WORKDIR /app

# Copy only requirements.txt first (rest will be mounted at runtime)

COPY requirements.txt /app/

# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Keep the container open for work

CMD ["/bin/bash"]

4. Create a Docker Compose File

To simplify running the container, create a file named docker-compose.yml in the same directory and add the following:

version: "3.8"

services:
agentorg:
image: agentorg-python3.10
build: .
container_name: agentorg-container
volumes: - /Users/brandonbyrd/AgentFirst/Agent-First-Organization:/app
working_dir: /app
stdin_open: true
tty: true
command: /bin/bash

5. Build and Start the Container

Navigate to the project directory and run the following command to build and start the container in the background:

docker-compose up -d

6. Access the Container

Once the container is running, you can open a terminal inside it by running:

docker exec -it agentorg-container /bin/bash

Now, you can work inside the container!

7. Verifying Python and Dependencies

Once inside the container, verify Python and installed dependencies:

python --version
pip list

If your project requires a virtual environment, create and activate it:

python -m venv venv
source venv/bin/activate

8. Running Your Project

Run your application as usual. For example:

python main.py

For Django/Flask applications:

python manage.py runserver 0.0.0.0:8000

For FastAPI:

uvicorn app:app --host 0.0.0.0 --port 8000

9. Stopping and Removing the Container

When you're done working, stop the container with:

docker-compose down

This will stop and remove the running container.

10. Keeping the Container Running

If you want to detach from the container while keeping it running, press:

Ctrl + P, then Ctrl + Q

To re-enter the container later, run:

docker exec -it agentorg-container /bin/bash

Conclusion

This setup ensures a consistent development environment using Docker. Your code is automatically mounted inside the container, allowing you to edit files locally while running your project in a controlled environment.

Happy coding! 🚀
