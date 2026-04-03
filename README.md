# Water Quality Classification

Predicting groundwater quality levels in Mexico using a Decision Tree and a Neural Network.

## Overview

This project uses chemical measurements from 2,728 groundwater monitoring sites across Mexico (2012–2024) to classify water quality into three levels based on the official SEMÁFORO (traffic light) indicator:

| Label | Meaning |
|---|---|
| VERDE (0) | Good quality — safe for drinking |
| AMARILLO (1) | Moderate concern — one or more parameters above limit |
| ROJO (2) | Poor quality — multiple parameters exceed safety limits |

## Results

| Metric | Score |
|---|---|
| Train accuracy | ~94% |
| Test accuracy | ~94% |

## Project Structure

```
├── data/
│   └── water_quality.xlsx       # Download separately (see below)
├── icon/
│   └── favicon.png
├── models/
│   ├── Decision-Tree_GroundWater-Model.joblib
│   ├── model_weights.pth
│   └── scaler.pkl
├── mexico_groundwater_quality_classification.ipynb
├── main.py                      # FastAPI app
├── requirements.txt
└── .gitignore
```

## Data

Download the dataset from CONAGUA (Mexico's National Water Commission):

-> https://www.gob.mx/conagua/es/articulos/indicadores-de-calidad-del-agua?idiom=es

Scroll to the last section: **"Indicadores de la calidad del agua subterránea a nivel nacional"**. Download the file under **B. Periodo 2012-2024 → Calidad del Agua Subterránea (Excel)**.

Place it in the `data/` folder and rename it `water_quality.xlsx`.

## How to Run

### Notebook

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the data (see above) and place it in `data/water_quality.xlsx`

4. Open the notebook:
```bash
jupyter notebook mexico_groundwater_quality_classification.ipynb
```

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

The model is trained on 14 chemical parameters including alkalinity, conductivity, dissolved solids, fluorides, hardness, fecal coliforms, nitrates, arsenic, cadmium, chromium, mercury, lead, manganese, and iron.
