FROM python:3.11-slim

# Linux updates aur Chromium browser system-level par install karne ke liye
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Sabhi python libraries install karne ke liye
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pura project code copy karne ke liye
COPY . .

# Hugging face container port expose karne ke liye
EXPOSE 7860

CMD ["python", "app.py"]