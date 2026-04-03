from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import joblib
import torch
import torch.nn as nn
import numpy as np
import pandas as pd

app = FastAPI()

# --- Feature order ---
FEATURE_ORDER = [
    'ALC_mg/L',
    'CONDUCT_mS/cm',
    'SDT_mg/L',
    'FLUORUROS_mg/L',
    'DUR_mg/L',
    'COLI_FEC_NMP/100_mL',
    'N_NO3_mg/L',
    'AS_TOT_mg/L',
    'CD_TOT_mg/L',
    'CR_TOT_mg/L',
    'HG_TOT_mg/L',
    'PB_TOT_mg/L',
    'MN_TOT_mg/L', 
    'FE_TOT_mg/L',
]

# --- Neural Network definition ---
class WaterModel(nn.Module):
    def __init__(self, input_features, output_features, hidden_units):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(input_features, hidden_units),
            nn.BatchNorm1d(hidden_units),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_units, hidden_units),
            nn.BatchNorm1d(hidden_units),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_units, hidden_units // 2),
            nn.BatchNorm1d(hidden_units // 2),
            nn.ReLU(),
            nn.Linear(hidden_units // 2, output_features)
        )

    def forward(self, x):
        return self.linear_layer_stack(x)

# --- Pydantic schema: field names map to training columns ---
class Chemical_Data(BaseModel):
    ALC_mg_L: float = Field(..., ge=0)          # Alcalinidad
    CONDUCT_mS_cm: float = Field(..., ge=0)     # Conductividad
    SDT_mg_L: float = Field(..., ge=0)          # Sólidos Disueltos Totales
    FLUORUROS_mg_L: float = Field(..., ge=0)    # Fluoruros
    DUR_mg_L: float = Field(..., ge=0)          # Dureza
    COLI_FEC_NMP_100_mL: float = Field(..., ge=0) # Coliformes Fecales
    N_NO3_mg_L: float = Field(..., ge=0)        # Nitratos
    AS_TOT_mg_L: float = Field(..., ge=0)       # Arsénico
    CD_TOT_mg_L: float = Field(..., ge=0)       # Cadmio
    CR_TOT_mg_L: float = Field(..., ge=0)       # Cromo
    HG_TOT_mg_L: float = Field(..., ge=0)       # Mercurio
    PB_TOT_mg_L: float = Field(..., ge=0)       # Plomo
    MN_TOT_mg_L: float = Field(..., ge=0)       # Manganeso 
    FE_TOT_mg_L: float =Field(..., ge=0)        # Hierro

    def to_dataframe(self) -> pd.DataFrame:
        """Return a single-row DataFrame with the exact column names used at training."""
        return pd.DataFrame([{
            'ALC_mg/L':              self.ALC_mg_L,
            'CONDUCT_mS/cm':         self.CONDUCT_mS_cm,
            'SDT_mg/L':              self.SDT_mg_L,
            'FLUORUROS_mg/L':        self.FLUORUROS_mg_L,
            'DUR_mg/L':              self.DUR_mg_L,
            'COLI_FEC_NMP/100_mL':   self.COLI_FEC_NMP_100_mL,
            'N_NO3_mg/L':            self.N_NO3_mg_L,
            'AS_TOT_mg/L':           self.AS_TOT_mg_L,
            'CD_TOT_mg/L':           self.CD_TOT_mg_L,
            'CR_TOT_mg/L':           self.CR_TOT_mg_L,
            'HG_TOT_mg/L':           self.HG_TOT_mg_L,
            'PB_TOT_mg/L':           self.PB_TOT_mg_L,
            'MN_TOT_mg/L':           self.MN_TOT_mg_L,
            'FE_TOT_mg/L':           self.FE_TOT_mg_L,
        }])

# --- Load Decision Tree model ---
dt_model = joblib.load("models/Decision-Tree_GroundWater-Model.joblib")

# --- Load scaler for Neural Network ---
scaler = joblib.load("models/scaler.pkl")

# --- Load Neural Network model ---
INPUT_FEATURES = 14
OUTPUT_FEATURES = 3
HIDDEN_UNITS = 64

nn_model = WaterModel(INPUT_FEATURES, OUTPUT_FEATURES, HIDDEN_UNITS)
state_dict = torch.load("models/model_weights.pth", map_location=torch.device("cpu"))
nn_model.load_state_dict(state_dict)
nn_model.eval()

# --- Class mapping ---
mapping = {'VERDE': 0, 'AMARILLO': 1, 'ROJO': 2}
inv_mapping = {v: k for k, v in mapping.items()}  # {0: 'VERDE', 1: 'AMARILLO', 2: 'ROJO'}

# --- Endpoints ---
@app.get("/")
def index():
    return {"message": "Welcome to the GroundWater Prediction API"}

@app.get("/favicon.ico")
def favicon():
    return FileResponse("icon/favicon.png")

@app.post("/predict/dt")
def predict_dt(data: Chemical_Data):
    # Pass a named DataFrame so the DT gets the same feature names it was trained on
    df = data.to_dataframe()
    pred_num = int(dt_model.predict(df)[0])  # np.int64 → Python int
    return {"prediction": inv_mapping[pred_num]}

@app.post("/predict/nn")
def predict_nn(data: Chemical_Data):
    df = data.to_dataframe()
    features_scaled  = scaler.transform(df)   # scaler also expects named columns
    features_tensor  = torch.tensor(features_scaled, dtype=torch.float32)

    with torch.inference_mode():
        pred_num = nn_model(features_tensor).argmax(dim=1).item()

    return {"prediction": inv_mapping[pred_num]}