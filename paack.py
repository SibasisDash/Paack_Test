# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
from datetime import datetime

df = pd.read_csv("packages_by_drivers_20200620.csv")

df['delivery_date'] = pd.to_datetime(df['delivery_date'])

#To find the start and end time
df_L = df.loc[df.groupby('driver_name').delivery_date.idxmin()].reset_index(drop=True)
df_H = df.loc[df.groupby('driver_name').delivery_date.idxmax()].reset_index(drop=True)

sum_package = df.groupby('driver_name')['num_packages_delivered'].sum()

def productivity(hours,package_driver):
    avg_prod = package_driver/hours
    return avg_prod

def no_of_hours(driver_name):
    start_time = df_L.delivery_date[df_L['driver_name'] == driver_name]
    end_time = df_H.delivery_date[df_H['driver_name'] == driver_name]
    if end_time.dt.minute.any() or end_time.dt.second.any():
        end_time = end_time.dt.hour + 1
    else:
        end_time = end_time.dt.hour 
    h = end_time - start_time.dt.hour
    return h

for i in range(len(sum_package)):
    driver_name = sum_package.index[i]
    hours = no_of_hours(driver_name)
    package_driver = sum_package[i]
    prod = productivity(hours,package_driver)
    
    print(driver_name,": ",prod.get(key=i))

