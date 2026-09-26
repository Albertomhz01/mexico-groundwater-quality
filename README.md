# AquaWatch MX — Groundwater Quality Classification

<<<<<<< HEAD
Predicting groundwater quality levels in Mexico using a Decision Tree and a Neural Network.
=======
Full-stack deployment of a groundwater quality classifier (Decision Tree + Neural Network) with a FastAPI backend and an Nginx-served dashboard frontend.
>>>>>>> 4872af0 (Docker and Frontend added)

## Project structure

```
<<<<<<< HEAD
├── data/
│   └── Calidad_del_Agua_Subterr_nea_p_2012-2024_15082025.xlsx       # Download separately (see below)
├── icon/
│   └── favicon.png
├── models/
│   ├── Decision-Tree_GroundWater-Model.joblib
│   ├── model_weights.pth
│   └── scaler.pkl
├── mexico_groundwater_quality_classification.ipynb
├── main.py                      # FastAPI app
=======
aquawatch/
├── main.py                   # FastAPI backend
>>>>>>> 4872af0 (Docker and Frontend added)
├── requirements.txt
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── models/
│   ├── Decision-Tree_GroundWater-Model.joblib
│   ├── model_weights.pth
│   └── scaler.pkl
├── icon/
│   └── favicon.png
├── frontend/
│   └── index.html            # Dashboard UI
└── nginx/
    └── nginx.conf
```

## Quick start

### 1. Local dev (no Docker)

<<<<<<< HEAD
-> https://www.gob.mx/conagua/es/articulos/indicadores-de-calidad-del-agua?idiom=es

Scroll to the last section: **"Indicadores de la calidad del agua subterránea a nivel nacional"**. Download the file under **B. Periodo 2012-2024 → Calidad del Agua Subterránea (Excel)**.

Place it in the `data/` folder with the name of `Calidad_del_Agua_Subterr_nea_p_2012-2024_15082025.xlsx`.

## How to Run

### Notebook

1. Clone the repository:
```bash
git clone https://github.com/Albertomhz01/mexico-groundwater-quality.git
cd mexico-groundwater-quality
```

2. Install dependencies:
=======
>>>>>>> 4872af0 (Docker and Frontend added)
```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend — just open frontend/index.html in your browser
# The dashboard calls http://localhost:8000 directly
```

### 2. Docker Compose (production-style)

```bash
# Build and start both services
docker compose up --build

# Frontend available at:  http://localhost
# Backend API at:         http://localhost:8000
# API docs at:            http://localhost:8000/docs
```

<<<<<<< HEAD
### API

The project also includes a FastAPI app that exposes both models as REST endpoints.

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `/docs`.

#### Endpoints

| Method | Path | Model |
|---|---|---|
| GET | `/` | Health check |
| POST | `/predict/dt` | Decision Tree |
| POST | `/predict/nn` | Neural Network |

Both prediction endpoints accept the same JSON body with 14 chemical parameters and return one of `VERDE`, `AMARILLO`, or `ROJO`.

#### Example request

```bash
curl -X POST "http://127.0.0.1:8000/predict/dt" \
  -H "Content-Type: application/json" \
  -d '{
    "ALC_mg_L": 180.0,
    "CONDUCT_mS_cm": 0.5,
    "SDT_mg_L": 320.0,
    "FLUORUROS_mg_L": 0.4,
    "DUR_mg_L": 200.0,
    "COLI_FEC_NMP_100_mL": 0.0,
    "N_NO3_mg_L": 2.1,
    "AS_TOT_mg_L": 0.001,
    "CD_TOT_mg_L": 0.0,
    "CR_TOT_mg_L": 0.0,
    "HG_TOT_mg_L": 0.0,
    "PB_TOT_mg_L": 0.0,
    "MN_TOT_mg_L": 0.01,
    "FE_TOT_mg_L": 0.05
  }'
```

#### Example response

```json
{"prediction": "VERDE"}
```

## Features Used

The model is trained on 14 chemical parameters: alkalinity, conductivity, dissolved solids, fluorides, hardness, fecal coliforms, nitrates, arsenic, cadmium, chromium, mercury, lead, manganese, and iron.
=======
```bash
# Stop
docker compose down

# Rebuild after code changes
docker compose up --build --force-recreate
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/predict/dt` | Decision Tree prediction |
| POST | `/predict/nn` | Neural Network prediction |

### Example request body

```json
{
  "ALC_mg_L": 200,
  "CONDUCT_mS_cm": 0.5,
  "SDT_mg_L": 500,
  "FLUORUROS_mg_L": 0.5,
  "DUR_mg_L": 200,
  "COLI_FEC_NMP_100_mL": 0,
  "N_NO3_mg_L": 3.0,
  "AS_TOT_mg_L": 0.005,
  "CD_TOT_mg_L": 0.001,
  "CR_TOT_mg_L": 0.01,
  "HG_TOT_mg_L": 0.0001,
  "PB_TOT_mg_L": 0.003,
  "MN_TOT_mg_L": 0.02,
  "FE_TOT_mg_L": 0.08
}
```

### Example response

```json
{ "prediction": "VERDE" }
```

## Classification legend

| Class | Meaning |
|-------|---------|
| `VERDE` | Water is suitable for human consumption |
| `AMARILLO` | Requires treatment before use |
| `ROJO` | Not suitable — high sanitary risk |

## Dashboard features

- Switch between Decision Tree and Neural Network models
- Bar chart showing parameter values normalized against NOM-127 limits
  (bars exceeding 100% are highlighted in red)
- "Load sample" cycles through example VERDE / AMARILLO / ROJO inputs
- Session history table with the last 10 predictions

## Production notes

- In `docker-compose.yml`, remove the `ports: - "8000:8000"` line under `backend`
  so the API is only accessible through Nginx, not directly from the internet.
- The Nginx config proxies `/api/*` → `http://backend:8000/`. If you update the
  frontend to use `/api/predict/dt` instead of `http://localhost:8000/predict/dt`,
  you can drop the direct port exposure entirely.
- Add HTTPS via Certbot/Let's Encrypt on the Nginx container for production.
>>>>>>> 4872af0 (Docker and Frontend added)
