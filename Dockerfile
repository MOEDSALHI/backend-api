# Use the official Python 3.12 image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the necessary files for dependency installation
COPY pyproject.toml poetry.lock ./

# Install dependencies with Poetry
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the project
COPY . .

# Grant execution permissions to entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the Django port
EXPOSE 8000

# Specify the entry point
ENTRYPOINT ["/app/entrypoint.sh"]
