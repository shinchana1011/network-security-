# 🛡️ Network Security — Phishing URL Detection

An end-to-end machine learning pipeline that detects phishing websites/URLs from structured URL and page features. The project covers the full ML lifecycle — data ingestion from MongoDB, automated data validation and transformation, model training with experiment tracking, and deployment as a REST API — packaged and shipped via Docker and CI/CD to AWS ECR.

## Overview

Phishing websites are a major attack vector in network security. This project treats phishing detection as a binary classification problem: given a set of extracted URL/page features, predict whether a site is legitimate or a phishing attempt.

Rather than a single notebook, the project is built as a modular, production-style Python package (`Networksecurity/`) with clearly separated stages: ingestion, validation, transformation, training, and inference — so each stage can be tested, reused, and monitored independently.

## Dataset

The model is trained on the **Phishing Websites Dataset**, a publicly available dataset (originally published via the UCI Machine Learning Repository, also mirrored on Kaggle). It contains 30 URL- and page-based binary/categorical features — such as `having_IP_Address`, `URL_Length`, `Shortining_Service`, `having_At_Symbol`, `SSLfinal_State`, `having_Sub_Domain`, `Request_URL`, `URL_of_Anchor`, `Abnormal_URL`, and `Links_in_tags` — used to classify a website as legitimate (`1`) or phishing (`-1`). The raw data (`network_data/phisingData.csv`) is ingested into MongoDB, from where the pipeline pulls it for validation and training.

## Features

- **Data ingestion** from a MongoDB collection into a versioned feature store
- **Schema-based data validation** (`data_schema/schema.yaml`) to catch drift or malformed input before training
- **Data transformation** pipeline (imputation/encoding/scaling) preceding model training
- **Model training** with experiment tracking via **MLflow** (integrated with **DagsHub** for remote tracking)
- **Artifact syncing to AWS S3** (`cloud/s3_syncer.py`) for backing up pipeline artifacts and models
- **Custom exception handling and logging** throughout the pipeline for easier debugging
- **FastAPI service** exposing:
  - `GET /train` — triggers the full training pipeline on demand
  - `POST /predict` — accepts a CSV of URL features and returns predictions rendered as an HTML table, plus a saved `prediction_output/output.csv`
- **Containerized with Docker** and **deployed via GitHub Actions CI/CD to AWS ECR**

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Data storage | MongoDB (`pymongo`), AWS S3 |
| ML / Data | scikit-learn, pandas, numpy |
| Experiment tracking | MLflow + DagsHub |
| API | FastAPI, Uvicorn, Jinja2 templates |
| Containerization | Docker |
| CI/CD | GitHub Actions → AWS ECR |
| Config | python-dotenv, PyYAML |

## Project Structure
```
network-security-/
├── Networksecurity/
│   ├── cloud/           # AWS S3 artifact syncing (s3_syncer.py)
│   ├── components/      # data_ingestion, data_validation, data_transformation, model_trainer
│   ├── constant/        # Pipeline-wide constants
│   ├── entity/          # Config & artifact entity classes
│   ├── exception/       # Custom NetworkSecurityException
│   ├── logging/         # Centralized logger
│   ├── pipeline/        # TrainingPipeline orchestration
│   └── utils/           # ML utils (model estimator, object load/save)
│
├── data_schema/
│   └── schema.yaml      # Expected feature schema for validation
│
├── network_data/
│   └── phisingData.csv  # Raw phishing dataset
│
├── valid.csv/
│   └── test.csv         # Validated/test split from the validation stage
│
├── final_model/         # Serialized preprocessor.pkl and model.pkl
├── prediction_output/   # Saved prediction CSVs
├── templates/           # Jinja2 HTML templates (results table)
│
├── .github/
│   └── workflows/
│       └── main.yml     # CI/CD: build, push to ECR, deploy
│
├── app.py               # FastAPI application (train/predict routes)
├── main.py              # CLI entry point to run the training pipeline
├── push_data.py         # Script to push local CSV data into MongoDB
├── test_mongodb.py      # MongoDB connection test script
├── setup.py             # Package setup
├── mlflow.db            # Local MLflow tracking store
├── Dockerfile
├── requirements.txt
└── .gitignore
```
## How It Works

1. **Ingestion** — `DataIngestion` pulls records from a MongoDB collection into a pandas DataFrame and writes them to a feature store.
2. **Validation** — `DataValidation` checks the ingested data against `data_schema/schema.yaml` to catch missing columns or schema drift.
3. **Transformation** — `DataTransformation` cleans and encodes the validated data into a model-ready format.
4. **Training** — `ModelTrainer` fits a classifier on the transformed data and logs parameters/metrics to MLflow (via DagsHub); the trained model and preprocessor are serialized to `final_model/`.
5. **Serving** — `app.py` loads the serialized model and preprocessor to serve real-time predictions through `/predict`, and can re-trigger training on demand through `/train`.

## Running Locally

```bash
git clone https://github.com/shinchana1011/network-security-.git
cd network-security-
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with your MongoDB connection string:

## License
This project is intended for academic and educational purposes.

