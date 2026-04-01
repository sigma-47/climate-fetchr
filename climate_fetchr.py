# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.


Stores in database by site number. 
Stores data back to Jan 1 of first plant
year.
On call it grabs existing data 



"""
import requests
import pandas as pd
from datetime import datetime as dt, timedelta as td
from matplotlib import pyplot as plt





def get_weather_data(lat, lon, start_date, end_date, data_type):
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto",
        "temperature_unit": "fahrenheit", # Change to 'celsius' if preferred
        "wind_speed_unit": "mph",        # Change to 'kmh' if preferred
        "precipitation_unit": "inch"      # Change to 'mm' if preferred
    }
        
    if data_type == 'historical':
        params["start_date"]=start_date
        params["end_date"]=end_date
        # API Endpoint for Historical Data
        url = "https://archive-api.open-meteo.com/v1/archive"
        #url = "https://api.open-meteo.com/v1/archive"
    else:
        url = "https://api.open-meteo.com/v1/forecast"
        params["models"] = "gfs_seamless"
        params["forecast_days"] = 7
        
    response = requests.get(url, params=params)
    data = response.json()
    
    # Convert the 'daily' dictionary into a Pandas DataFrame
    df = pd.DataFrame(data['daily'])
    df = df.rename(columns={'time':'date'})
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['type'] = data_type
    
    return df

# Example: Minneapolis (your home area)
LAT, LON = 44.9778, -93.2650

list()
beg = dt.today()-td(days=15*365)
beg = dt.strptime("01-01-2025", "%m-%d-%Y")
end = dt.today()


START, END = beg.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

DTYPE = "historical"

data_df = get_weather_data(LAT, LON, START, END, DTYPE)
print(data_df)

DTYPE = "forecast"
data_df = pd.concat([data_df, get_weather_data(LAT, LON, START, END, DTYPE)],
                       axis=0)

fig, ax = plt.subplots(figsize=(11,8.5))


ax = data_df.loc[beg:end]['temperature_2m_max'].plot(ax=ax, color='red', linestyle='-')

ax = data_df[data_df['type']=='forecast']['temperature_2m_max'].plot(ax=ax, color='red', linestyle='--')

ax = data_df.loc[beg:end]['temperature_2m_min'].plot(ax=ax, color='blue', linestyle='-')

ax = data_df[data_df['type']=='forecast']['temperature_2m_min'].plot(ax=ax, color='blue', linestyle='--')

data_df.boxplot(column='precipitation_sum')

plt.show()
