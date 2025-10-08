# Stage 1: Build the MuseTalk environment
FROM python:3.10-slim AS musetalk_builder

WORKDIR /app

# Clone the MuseTalk repository
RUN apt-get update && apt-get install -y git build-essential
RUN git clone https://github.com/TMElyralab/MuseTalk.git

# Install MuseTalk dependencies
WORKDIR /app/MuseTalk
RUN pip install -r requirements.txt
RUN pip install mmcv mmpose --no-deps

# Download the models
RUN chmod +x download_weights.sh
RUN bash ./download_weights.sh

# Stage 2: Build the final application image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 ffmpeg

WORKDIR /app

# Copy the pre-built MuseTalk environment
COPY --from=musetalk_builder /app/MuseTalk /app/MuseTalk
COPY --from=musetalk_builder /root/.cache /root/.cache
COPY --from=musetalk_builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy our application code
COPY . .

# Install our application's dependencies
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt_tab

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
