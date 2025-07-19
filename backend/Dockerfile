FROM python:3.12-slim

# 1) Install OS build tools & CMake for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./ ./

# 2) Then install Python deps
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
