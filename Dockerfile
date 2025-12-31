# 1. Base image
FROM python:3.13-slim

# 2. Work directory inside container
WORKDIR /app

# 3. Install system dependencies (optional, but often useful)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements and install Python deps
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Environment variables for production
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 7. Expose port 5000 (container side)
EXPOSE 5000

# 8. Start Gunicorn, telling it where to find your app object
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
