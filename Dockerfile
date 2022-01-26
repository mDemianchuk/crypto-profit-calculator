FROM python:3.9-slim
# Set env vars
ENV APP_HOST 0.0.0.0
ENV APP_PORT 5000
ENV FLASK_APP /app/run.py
ENV FLASK_ENV development
ENV PYTHONPATH /usr/bin/python3.9
ENV PYTHONUNBUFFERED 1
# Copy the dependencies file
COPY Pipfile .
# Install pipenv
RUN pip install --upgrade pip && pip install pipenv
# Install dependencies
RUN pipenv install --system --skip-lock
# Make the 'app' folder the current working directory
WORKDIR /app
# Copy the source code
COPY app/ .
# Start the application server
CMD ["sh", "-c", "flask run -h $APP_HOST -p $APP_PORT"]
