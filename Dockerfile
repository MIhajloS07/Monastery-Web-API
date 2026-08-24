# python image
FROM python:3.12-slim

# working directory
WORKDIR /app

# copy requirements and install 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# use port 5000
EXPOSE 5000

# Start Flask WebAPI
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
