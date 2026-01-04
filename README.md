# kurdistan-covid-seir-arima-2025
# COVID-19 Modeling in Kurdistan Province: SEIR and ARIMA Analysis

This repository contains the complete code and synthetic data to reproduce the results and **Figure 1** presented in the manuscript:

*"Modeling the COVID-19 Epidemic in Kurdistan Province Using the SEIR Model and Time Series Analysis of Hospitalized Patients During the First Wave"*

## Key Features
- Deterministic SEIR model with absolute compartment sizes (population = 1,600,000)
- 95% confidence interval for the Infected compartment via Monte Carlo simulation (300 runs, 15% variation in β)
- Intervention onset marked on day 25 (March 16, 2020)
- ARIMA(1,1,1) forecast of daily hospitalizations with 95% confidence interval
- Combined two-panel Figure 1 exactly as shown in the manuscript

## Files
- `seir_model.py`: SEIR model with Monte Carlo 95% CI for Infected compartment
- `arima_forecast.py`: ARIMA(1,1,1) forecast of daily hospitalizations
- `figure1_combined.py`: Generates the exact two-panel Figure 1 as in the manuscript
- `covid19_kurdistan_seir-arima.jpg`: High-resolution output of the combined figure (SEIR upper panel, ARIMA lower panel)
- `synthetic_hospitalizations.csv`: Synthetic daily hospitalization data preserving statistical properties and trends of the original anonymized series
- `requirements.txt`: Exact package versions for full reproducibility

## How to Reproduce
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows
