# 🛡️ Network Security — Phishing URL Detection

An end-to-end machine learning pipeline that detects phishing websites/URLs from structured URL and page features. The project covers the full ML lifecycle — data ingestion from MongoDB, automated data validation and transformation, model training with experiment tracking, and deployment as a REST API — packaged and shipped via Docker and CI/CD to AWS ECR.

## Overview

Phishing websites are a major attack vector in network security. This project treats phishing detection as a binary classification problem: given a set of extracted URL/page features, predict whether a site is legitimate or a phishing attempt.

Rather than a single notebook, the project is built as a modular, production-style Python package (`Networksecurity/`) with clearly separated stages: ingestion, validation, transformation, training, and inference — so each stage can be tested, reused, and monitored independently.

## Features

- **Data ingestion** from a MongoDB collection into a versioned feature store
- **Schema-based data validation** (`data_schema/schema.yaml`) to catch drift or malformed input before training
- **Data transformation** pipeline (imputation/encoding/scaling) preceding model training
- **Model training** with experiment tracking via **MLflow** (integrated with **DagsHub** for remote tracking)
- **Custom exception handling and logging** throughout the pipeline for easier debugging
- **FastAPI service** exposing:
  - `GET /train` — triggers the full training pipeline on demand
  - `POST /predict` — accepts a CSV of URL features and returns predictions rendered as an HTML table, plus a saved `prediction_output/output.csv`
- **Containerized with Docker** and **deployed via GitHub Actions CI/CD to AWS ECR**

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Data storage | MongoDB (`pymongo`) |
| ML / Data | scikit-learn, pandas, numpy |
| Experiment tracking | MLflow + DagsHub |
| API | FastAPI, Uvicorn, Jinja2 templates |
| Containerization | Docker |
| CI/CD | GitHub Actions → AWS ECR |
| Config | python-dotenv, PyYAML |

## Project Structure
network-security-/
├── Networksecurity/
│   ├── components/        # DataIngestion, DataValidation, DataTransformation, ModelTrainer
│   ├── entity/             # Config & artifact entity classes
│   ├── exception/          # Custom NetworkSecurityException
│   ├── logging/            # Centralized logger
│   ├── pipeline/           # TrainingPipeline orchestration
│   └── utils/               # ML utils (model estimator, object load/save)
├── data_schema/
│   └── schema.yaml         # Expected feature schema for validation
├── final_model/            # Serialized preprocessor.pkl and model.pkl
├── prediction_output/      # Saved prediction CSVs
├── templates/               # Jinja2 HTML templates (results table)
├── .github/workflows/
│   └── main.yml            # CI/CD: build, push to ECR, deploy
├── app.py                   # FastAPI application (train/predict routes)
├── main.py                  # CLI entry point to run the training pipeline
├── Dockerfile
└── requirements.txt

## How It Works

1. **Ingestion** — `DataIngestion` pulls records from a MongoDB collection into a pandas DataFrame and writes them to a feature store.
2. **Validation** — `DataValidation` checks the ingested data against `data_schema/schema.yaml` to catch missing columns or schema drift.
3. **Transformation** — `DataTransformation` cleans and encodes the validated data into a model-ready format.
4. **Training** — `ModelTrainer` fits a classifier on the transformed data and logs parameters/metrics to MLflow (via DagsHub); the trained model and preprocessor are serialized to `final_model/`.
5. **Serving** — `app.py` loads the serialized model and preprocessor to serve real-time predictions through `/predict`, and can re-trigger training on demand through `/train`.

## Running Locally

```bash
# Clone and set up environment
git clone https://github.com/shinchana1011/network-security-.git
cd network-security-
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with your MongoDB connection string:
MONGODB_URL_KEY=<your-mongodb-connection-string>

Run the API:

```bash
python app.py
```

The app starts on `http://localhost:8080`. Visit `/docs` for interactive Swagger API docs, `/train` to run the training pipeline, or `POST` a CSV file to `/predict` for inference.

## Running with Docker

```bash
docker build -t network-security-app .
docker run -p 8080:8080 --env-file .env network-security-app
```

## CI/CD

Every push to `main` (excluding README changes) triggers a GitHub Actions workflow that builds the Docker image and pushes it to an AWS ECR repository, from which it is deployed — giving the project a full path from code commit to a running, containerized service.

## License
This project is intended for academic and educational purposes.

