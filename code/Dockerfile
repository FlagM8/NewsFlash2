# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /code

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5001

# Default command to run the application
CMD ["python", "main.py"]