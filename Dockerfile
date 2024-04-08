# Verwenden Sie das offizielle Python-Image als Basis
FROM python:3.9-slim

# Kopieren Sie die Anwendungsdateien in den Container
COPY . /app

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie die Anforderungen
RUN pip install --no-cache-dir -r requirements.txt

# Exponieren Sie den Port, den Ihr FastAPI-Server verwendet
EXPOSE 8080

# Befehl zum Ausführen Ihres FastAPI-Servers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]