# seir_model.py
# SEIR model with Monte Carlo 95% CI for Infected compartment

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def seir_model(state, t, beta, alpha, gamma, N):
    S, E, I, R = state
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - alpha * E
    dIdt = alpha * E - gamma * I
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

# Parameters
N = 1_600_000
beta = 0.30
alpha = 0.20
gamma = 0.10

I0 = 150
E0 = 300
R0 = 0
S0 = N - I0 - E0 - R0
state0 = [S0, E0, I0, R0]

days = 60
t = np.linspace(0, days, days)

# Solve deterministic SEIR
solution = odeint(seir_model, state0, t, args=(beta, alpha, gamma, N))
S, E, I, R = solution.T

# Monte Carlo for 95% CI on Infected
n_sim = 300
beta_sd = 0.15 * beta
I_sim = np.zeros((n_sim, len(t)))
for i in range(n_sim):
    beta_i = np.random.normal(beta, beta_sd)
    sol_i = odeint(seir_model, state0, t, args=(beta_i, alpha, gamma, N))
    I_sim[i, :] = sol_i[:, 2]

I_lower = np.percentile(I_sim, 2.5, axis=0)
I_upper = np.percentile(I_sim, 97.5, axis=0)

# Dates and intervention
start_date = datetime(2020, 2, 20)
dates = [start_date + timedelta(days=int(x)) for x in t]
intervention_day = 25

# Plot SEIR only
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dates, S, label='Susceptible (S)', color='#1f77b4', linewidth=2.5)
ax.plot(dates, E, label='Exposed (E)', color='#ff7f0e', linewidth=2.5)
ax.plot(dates, I, label='Infected (I)', color='#2ca02c', linewidth=3)
ax.fill_between(dates, I_lower, I_upper, color='#2ca02c', alpha=0.2, label='95% CI (Infected)')
ax.plot(dates, R, label='Recovered (R)', color='#d62728', linewidth=2.5)
ax.axvline(dates[intervention_day], color='black', linestyle='--', alpha=0.7, label='Intervention onset')

ax.set_title('SEIR Model - Absolute Numbers with 95% CI for Infected', fontsize=14)
ax.set_ylabel('Number of Individuals')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('seir_plot.jpg', dpi=400)
plt.close()

print("SEIR plot saved as seir_plot.jpg")