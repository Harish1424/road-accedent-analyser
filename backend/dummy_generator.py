import pandas as pd
import numpy as np
import datetime

def generate_dummy_data(n_samples=180):
    np.random.seed(42)
    start_date = datetime.date(2025, 1, 1)
    dates = [start_date + datetime.timedelta(days=int(np.random.randint(0, 180))) for _ in range(n_samples)]
    times = [f"{np.random.randint(0, 24):02d}:{np.random.choice([0, 15, 30, 45]):02d}" for _ in range(n_samples)]
    locations = [
        ("Central Avenue Expressway", 12.9716, 77.5946),
        ("Outer Ring Flyover", 12.9352, 77.6245),
        ("Tech Park Junction", 12.9850, 77.7300),
        ("Northern Bypass Highway", 13.0358, 77.5970),
        ("South Terminal Link", 12.9166, 77.6101),
        ("Industrial Corridor West", 12.9600, 77.5100),
        ("Metro Corridor Junction", 12.9780, 77.6400),
        ("East Coastal Boulevard", 12.9900, 77.6800),
        ("Old City Intersection", 12.9550, 77.5750),
        ("Airport Express Highway", 13.1000, 77.6000)
    ]
    selected_locs = [locations[np.random.randint(0, len(locations))] for _ in range(n_samples)]
    loc_names = [l[0] for l in selected_locs]
    lats = [l[1] + np.random.normal(0, 0.008) for l in selected_locs]
    lons = [l[2] + np.random.normal(0, 0.008) for l in selected_locs]
    fatalities = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.75, 0.18, 0.05, 0.02])
    injuries = np.random.choice([0, 1, 2, 3, 4, 5], size=n_samples, p=[0.3, 0.35, 0.2, 0.1, 0.03, 0.02])
    costs = np.round(np.random.uniform(5000, 250000, size=n_samples), 2)
    road_types = np.random.choice(["Highway", "Urban Road", "Rural Road", "Intersection", "Expressway"], size=n_samples, p=[0.35, 0.25, 0.15, 0.15, 0.10])
    weather_conds = np.random.choice(["Clear", "Rainy", "Foggy", "Snow", "Stormy"], size=n_samples, p=[0.55, 0.25, 0.12, 0.03, 0.05])
    df = pd.DataFrame({
        "Date": dates,
        "Time": times,
        "Location_Name": loc_names,
        "Latitude": lats,
        "Longitude": lons,
        "Injuries": injuries,
        "Fatalities": fatalities,
        "Material_Loss_Cost": costs,
        "Road_Type": road_types,
        "Weather_Condition": weather_conds
    })
    return df
