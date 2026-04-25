FROM mcr.microsoft.com/playwright/python:v1.58.0-noble

WORKDIR /app

COPY pyproject.toml README.md main.py ./
COPY aeza_monitor ./aeza_monitor

RUN pip install --no-cache-dir "playwright>=1.58.0" "requests>=2.32.0"

CMD ["python", "main.py"]
