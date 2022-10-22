# Set base image (host OS)
FROM python:3.10-buster

# By default, listen on port 5000
EXPOSE 80/tcp

# Set the working directory in the container
WORKDIR /bussie_backend

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY gunicorn.sh .
COPY main.py .
COPY static ./static
# Specify the command to run on container start
ENTRYPOINT ["./gunicorn.sh"]
