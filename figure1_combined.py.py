# figure1_combined.py
# Generates the exact two-panel Figure 1 as in the manuscript

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

# ================== SEIR Section ==================
def seir_model(state, t, beta, alpha, gamma, N):
    S, E, I, R = state
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - alpha * E
    dIdt = alpha * E - gamma * I
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

N = 1_600_000
beta = 0.30
alpha = 0.20
gamma = 0.10
I0, E0, R0 = 150, 300, 0
S0 = N - I0 - E0 - R0
state0 = [S0, E0, I0, R0]

t = np.linspace(0, 60, 60)
solution = odeint(seir_model, state0, t, args=(beta, alpha, gamma, N))
S, E, I, R = solution.T

# Monte Carlo CI
n_sim = 300
beta_sd = 0.15 * beta
I_sim = np.zeros((n_sim, len(t)))
for i in range(n_sim):
    beta_i = np.random.normal(beta, beta_sd)
    sol_i = odeint(seir_model, state0, t, args=(beta_i, alpha, gamma, N))
    I_sim[i, :] = sol_i[:, 2]
I_lower = np.percentile(I_sim, 2.5, axis=0)
I_upper = np.percentile(I_sim, 97.5, axis=0)

start_date = datetime(2020, 2, 20)
dates = [start_date + timedelta(days=int(x)) for x in t]
intervention_day = 25

# ================== ARIMA Section ==================
df_hosp = pd.read_csv('synthetic_hospitalizations.csv', parse_dates=['Date'])
df_hosp = df_hosp.set_index('Date')
hospitalizations = df_hosp['Hospitalizations']

arima_model = ARIMA(hospitalizations, order=(1, 1, 1))
arima_fit = arima_model.fit()

forecast_steps = 20
forecast = arima_fit.get_forecast(steps=forecast_steps)
arima_mean = forecast.predicted_mean
arima_ci = forecast.conf_int(alpha=0.05)
forecast_dates = pd.date_range(start=hospitalizations.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

# ================== Combined Figure 1 ==================
fig = plt.figure(figsize=(14, 10))

# Upper panel: SEIR
ax1 = fig.add_subplot(2, 1, 1)
ax1.plot(dates, S, label='Susceptible (S)', color='#1f77b4', linewidth=2.5)
ax1.plot(dates, E, label='Exposed (E)', color='#ff7f0e', linewidth=2.5)
ax1.plot(dates, I, label='Infected (I)', color='#2ca02c', linewidth=3)
ax1.fill_between(dates, I_lower, I_upper, color='#2ca02c', alpha=0.2, label='95% CI (Infected)')
ax1.plot(dates, R, label='Recovered (R)', color='#d62728', linewidth=2.5)
ax1.axvline(dates[intervention_day], color='black', linestyle='--', linewidth=1.5, alpha=0.7, label='Intervention onset')
ax1.set_title('Upper Panel: SEIR Model (Absolute Numbers with 95% CI for Infected)', fontsize=14)
ax1.set_ylabel('Number of Individuals')
ax1.legend(fontsize=11, loc='upper right')
ax1.grid(True, alpha=0.3)

# Lower panel: ARIMA
ax2 = fig.add_subplot(2, 1, 2)
ax2.bar(hospitalizations.index, hospitalizations, width=0.8, alpha=0.7, color='purple',
        label='Observed Daily Hospitalizations')
ax2.plot(forecast_dates, arima_mean, color='red', linestyle='--', linewidth=2.5,
         label='ARIMA(1,1,1) Forecast')
ax2.fill_between(forecast_dates, arima_ci.iloc[:, 0], arima_ci.iloc[:, 1],
                 color='pink', alpha=0.3, label='95% Confidence Interval')
ax2.set_title('Lower Panel: ARIMA Forecast of Daily Hospitalizations', fontsize=14)
ax2.set_xlabel('Date')
ax2.set_ylabel('Daily Hospitalizations')
ax2.legend(fontsize=11, loc='upper left')
ax2.grid(True, alpha=0.3)

# Common formatting
for ax in [ax1, ax2]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    plt.setp(ax.get_xticklabels(), rotation=45)

plt.suptitle('Figure 1: SEIR Model and ARIMA Forecast of the First COVID-19 Wave in Kurdistan Province', 
             fontsize=16, y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('figure1_combined.jpg', dpi=400, bbox_inches='tight')
plt.close()

print("Figure 1 (two-panel combined plot) saved as figure1_combined.jpg")