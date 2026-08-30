import pandas as pd

def calculate_severity(df):
    df_copy = df.copy()
    df_copy["Severity_Score"] = (df_copy["Fatalities"] * 10) + (df_copy["Injuries"] * 4) + (df_copy["Material_Loss_Cost"] / 10000.0)
    return df_copy
