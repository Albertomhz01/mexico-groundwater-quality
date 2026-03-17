# Water Quality Classification

Predicting groundwater quality levels in Mexico using a Decision Tree classifier.

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
│   └── water_quality.xlsx    # Download separately (see below)
├── mexico_groundwater_quality_classification.ipynb
├── requirements.txt
└── .gitignore
```

## Data

Download the dataset from CONAGUA (Mexico's National Water Commission):

👉 https://www.gob.mx/conagua/es/articulos/indicadores-de-calidad-del-agua?idiom=es

Scroll to the last section of the page: **"Indicadores de la calidad del agua subterránea a nivel nacional"**. Download the file under **B. Periodo 2012-2024 → Calidad del Agua Subterránea (Excel)**.

Once downloaded, place the file inside a `data/` folder in the project root and rename it `water_quality.xlsx`.

## How to Run

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

## Features Used

The model is trained on 14 chemical parameters including alkalinity, conductivity, dissolved solids, fluorides, hardness, fecal coliforms, nitrates, arsenic, cadmium, chromium, mercury, lead, manganese, and iron.
