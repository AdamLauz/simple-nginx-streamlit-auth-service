# Pull Python 3.10 image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Transfer content from current dir to /app in container
ADD . /app


# Install Python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Start uWSGI using the config file
CMD ["uwsgi", "app.ini"]