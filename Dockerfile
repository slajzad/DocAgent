FROM python:3.10-slim

# Add this line
RUN apt-get update && apt-get install -y curl

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt chromadb
COPY . .

# Copy and set the entrypoint
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]