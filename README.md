# kurdistan-covid-seir-arima-2025
# COVID-19 Modeling in Kurdistan Province: SEIR and ARIMA Analysis

This repository provides the complete computational workflow used in the manuscript:

**“Modeling the COVID-19 Epidemic in Kurdistan Province Using the SEIR Model and Time Series Analysis of Hospitalized Patients During the First Wave.”**

The aim of this repository is to enhance transparency, reproducibility, and methodological clarity of the SEIR simulation and ARIMA time-series analysis presented in the study, while fully respecting ethical and institutional constraints on patient-level data sharing.

---

## 🔑 Key Features

- Deterministic **SEIR compartmental model** with absolute population sizes (total population = 1,600,000)
- **Monte Carlo simulation** to construct a 95% confidence interval for the Infected compartment
- Explicit modeling of **intervention onset** during the first epidemic wave
- **ARIMA(1,1,1)** time-series modeling and short-term forecasting of daily hospitalizations with 95% confidence intervals
- Generation of the **combined two-panel Figure 1** (SEIR dynamics and ARIMA forecast) consistent with the manuscript

---

## 📂 Repository Contents

- `seir_model.py`  
  Implements the SEIR model and Monte Carlo uncertainty analysis.

- `arima_forecast.py`  
  Performs ARIMA(1,1,1) modeling and forecasting of daily hospitalizations.

- `figure1_combined.py`  
  Generates the combined two-panel figure integrating SEIR results and ARIMA forecasts.

- `synthetic_hospitalizations.csv`  
  A synthetic daily hospitalization time series created solely for reproducibility purposes.  
  This dataset preserves **key aggregate statistical properties and broad temporal patterns** of the original anonymized data, without containing any real patient-level information.

- `covid19_kurdistan_seir-arima.jpg`  
  High-resolution output of the combined figure used in the manuscript.

- `requirements.txt`  
  Exact package versions used for all analyses.

- `README.md`  
  Documentation and reproduction instructions.

---

## 🔒 Data Availability and Ethics

The original hospital admission records contain sensitive patient-level information and **cannot be shared publicly** due to ethical and institutional regulations from Kurdistan University of Medical Sciences.

To support reproducibility without violating data privacy, a **synthetic hospitalization dataset** is provided. This dataset is intended **only to demonstrate the analytical workflow and reproduce the figures**, and it does not represent real patient data nor allow re-identification.

Researchers with appropriate authorization may apply the provided code to their own institutional datasets.

---

## ▶️ How to Reproduce the Analysis

1. Clone the repository:
   ```bash
   git clone https://github.com/eghbal1363-creator/kurdistan-covid-seir-arima-2025.git
   cd kurdistan-covid-seir-arima-2025
