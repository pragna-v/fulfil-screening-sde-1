# Fulfil Screening Task – SDE 1 (Python Full Stack)

This project is a CSV product importer built with:

- **FastAPI** (backend)
- **Celery** (background processing)
- **Redis** (task queue)
- **PostgreSQL** (database)
- **Docker & Docker Compose** (containerized setup)
- **HTML + JS** (CSV upload UI with real-time progress bar)

---

## 🚀 Features

- CSV upload with expected headers:
- Background processing using Celery (good for large files)
- Real-time progress updates via Server-Sent Events (SSE)
- Case-insensitive SKU uniqueness via DB index/upsert
- Web UI for uploading CSVs and monitoring progress

---

## 📂 Project Structure
app/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── crud.py
└── tasks.py
frontend/
└── upload.html
Dockerfile
docker-compose.yml
requirements.txt
README.md

---

## 🐳 Running the Project (local)

1. Start everything using Docker:
   ```bash
   docker compose up --build
   http://localhost:8000
sku,name,description,price,active
SKU1,Product A,Description A,10.99,true
SKU2,Product B,Description B,20.00,false
SKU3,Product C,Description C,15.50,true
---

## 👤 Author

**Vulli Pragna**  
Email: vullipragna19@gmail.com


