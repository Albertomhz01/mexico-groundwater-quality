# AquaWatch MX — Groundwater Quality Classification

Predicting groundwater quality levels in Mexico using a Decision Tree and a Neural Network, deployed as a full-stack app with a FastAPI backend and an Nginx-served dashboard frontend.

## Project structure

```
├── data/
│   └── Calidad_del_Agua_Subterr_nea_p_2012-2024_15082025.xlsx   # Download separately (see below)
├── frontend/
│   └── index.html                # Dashboard UI
├── icon/
│   └── favicon.png
├── models/
│   ├── Decision-Tree_GroundWater-Model.joblib
│   ├── model_weights.pth
│   └── scaler.pkl
├── nginx/
│   └── nginx.conf
├── mexico_groundwater_quality_classification.ipynb
├── main.py                       # FastAPI backend
├── requirements.txt
├── Dockerfile.backend
├── Dockerfile.frontend
└── docker-compose.yml
```

## Dataset

The data comes from CONAGUA's water quality indicators:

-> https://www.gob.mx/conagua/es/articulos/indicadores-de-calidad-del-agua?idiom=es

Scroll to the last section: **"Indicadores de la calidad del agua subterránea a nivel nacional"**. Download the file under **B. Periodo 2012-2024 → Calidad del Agua Subterránea (Excel)**.

Place it in the `data/` folder with the name `Calidad_del_Agua_Subterr_nea_p_2012-2024_15082025.xlsx`.

The dataset is only needed to run the notebook. The API and dashboard use the pretrained models in `models/`.

## Getting started

Clone the repository:

```bash
git clone https://github.com/Albertomhz01/mexico-groundwater-quality.git
cd mexico-groundwater-quality
```

### Option 1: Notebook

```bash
pip install -r requirements.txt
jupyter notebook mexico_groundwater_quality_classification.ipynb
```

### Option 2: Local dev (no Docker)

```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open `frontend/index.html` in your browser. The dashboard calls `http://localhost:8000` directly.

### Option 3: Docker Compose (production-style)

```bash
# Build and start both services
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

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

Both prediction endpoints accept the same JSON body with 14 chemical parameters and return one of `VERDE`, `AMARILLO`, or `ROJO`.

### Example request

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

### Example response

```json
{ "prediction": "VERDE" }
```

## Features used

The models are trained on 14 chemical parameters: alkalinity, conductivity, dissolved solids, fluorides, hardness, fecal coliforms, nitrates, arsenic, cadmium, chromium, mercury, lead, manganese, and iron.

## Classification legend

| Class | Meaning |
|-------|---------|
| `VERDE` | Water is suitable for human consumption |
| `AMARILLO` | Requires treatment before use |
| `ROJO` | Not suitable, high sanitary risk |

## Dashboard features

- Switch between Decision Tree and Neural Network models
- Bar chart showing parameter values normalized against NOM-127 limits (bars exceeding 100% are highlighted in red)
- "Load sample" cycles through example VERDE / AMARILLO / ROJO inputs
- Session history table with the last 10 predictions

## Production notes

- In `docker-compose.yml`, remove the `ports: - "8000:8000"` line under `backend` so the API is only accessible through Nginx, not directly from the internet.
- The Nginx config proxies `/api/*` → `http://backend:8000/`. If you update the frontend to use `/api/predict/dt` instead of `http://localhost:8000/predict/dt`, you can drop the direct port exposure entirely.
- Add HTTPS via Certbot/Let's Encrypt on the Nginx container for production.
