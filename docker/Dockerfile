FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

# Set non-interactive mode to prevent tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install required dependencies for Python 3.10
RUN apt-get update && apt-get install -y \
    supervisor \
    curl \
    ffmpeg \
    software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev python3.10-distutils \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as default
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && ln -sf /usr/bin/python3.10 /usr/bin/python3

# Install pip for Python 3.10
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# # Preload the model during the Docker build stage
# RUN python3 -c "from essentia.standard import TensorflowPredictEffnetDiscogs, TensorflowPredict2D; \
#     TensorflowPredictEffnetDiscogs(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/discogs-effnet-bs64-1.pb', output='PartitionedCall:1'); \
#     TensorflowPredict2D(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/mtg_jamendo_genre-discogs-effnet-1.pb'); \
#     TensorflowPredict2D(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/mtg_jamendo_moodtheme-discogs-effnet-1.pb'); \
#     TensorflowPredict2D(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/mood_aggressive-discogs-effnet-1.pb', output='model/Softmax'); \
#     TensorflowPredict2D(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/engagement_regression-discogs-effnet-1.pb', output='model/Identity'); \
#     TensorflowPredict2D(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/mood_happy-discogs-effnet-1.pb', output='model/Softmax'); \
#     TensorflowPredict2D(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/mood_relaxed-discogs-effnet-1.pb', output='model/Softmax'); \
#     TensorflowPredict2D(graphFilename='/app/src/modules/songs/infrastructure/essentia_features/models/mood_sad-discogs-effnet-1.pb', output='model/Softmax'); \
#     print('✅ Model preloaded successfully in Docker!')"

COPY docker/supervisor/supervisor.conf /etc/supervisor/conf.d/supervisord.conf

# Start Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]