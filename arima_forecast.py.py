# arima_forecast.py
# ARIMA(1,1,1) forecast of daily hospitalizations

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings("ignore")

# Load synthetic data
df = pd.read_csv('synthetic_hospitalizations.csv', parse_dates=['Date'])
df = df.set_index('Date')
hospitalizations = df['Hospitalizations']

# Fit ARIMA(1,1,1)
model = ARIMA(hospitalizations, order=(1, 1, 1))
fit = model.fit()

# Forecast next 20 days
forecast_steps = 20
forecast_result = fit.get_forecast(steps=forecast_steps)
forecast_mean = forecast_result.predicted_mean
forecast_ci = forecast_result.conf_int(alpha=0.05)

# Forecast dates
last_date = hospitalizations.index[-1]
forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

# Plot
plt.figure(figsize=(12, 6))
plt.bar(hospitalizations.index, hospitalizations, width=0.8, alpha=0.7, color='purple',
        label='Observed Daily Hospitalizations')
plt.plot(forecast_dates, forecast_mean, color='red', linestyle='--', linewidth=2.5,
         label='ARIMA(1,1,1) Forecast')
plt.fill_between(forecast_dates, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1],
                 color='pink', alpha=0.3, label='95% Confidence Interval')

plt.title('ARIMA(1,1,1) Forecast of Daily Hospitalizations', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Daily Hospitalizations')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('arima_forecast.jpg', dpi=400)
plt.close()

print("ARIMA forecast plot saved as arima_forecast.jpg")