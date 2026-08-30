import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "accident_data.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Time TEXT,
        Location_Name TEXT,
        Latitude REAL,
        Longitude REAL,
        Injuries INTEGER,
        Fatalities INTEGER,
        Material_Loss_Cost REAL,
        Road_Type TEXT,
        Weather_Condition TEXT
    )
    """)
    conn.commit()
    conn.close()

def load_all_records():
    init_db()
    conn = get_connection()
    df = pd.read_sql_query("SELECT Date, Time, Location_Name, Latitude, Longitude, Injuries, Fatalities, Material_Loss_Cost, Road_Type, Weather_Condition FROM accidents", conn)
    conn.close()
    return df

def save_records(df):
    init_db()
    conn = get_connection()
    df.to_sql("accidents", conn, if_exists="replace", index=False)
    conn.close()

def add_record(record_dict):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO accidents (Date, Time, Location_Name, Latitude, Longitude, Injuries, Fatalities, Material_Loss_Cost, Road_Type, Weather_Condition)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(record_dict["Date"]),
        str(record_dict["Time"]),
        str(record_dict["Location_Name"]),
        float(record_dict["Latitude"]),
        float(record_dict["Longitude"]),
        int(record_dict["Injuries"]),
        int(record_dict["Fatalities"]),
        float(record_dict["Material_Loss_Cost"]),
        str(record_dict["Road_Type"]),
        str(record_dict["Weather_Condition"])
    ))
    conn.commit()
    conn.close()

def reset_database(df):
    save_records(df)
