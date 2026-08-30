import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def train_predictive_model(df):
    df_copy = df.copy()
    df_copy["Hour"] = pd.to_datetime(df_copy["Time"], format="%H:%M").dt.hour
    df_copy["Day_of_Week"] = pd.to_datetime(df_copy["Date"]).dt.day_name()
    X = df_copy[["Hour", "Day_of_Week", "Road_Type", "Weather_Condition"]]
    y = df_copy["Risk_Level"]
    categorical_features = ["Day_of_Week", "Road_Type", "Weather_Condition"]
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ],
        remainder="passthrough"
    )
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    model.fit(X, y)
    return model

def predict_scenario_risk(model, hour, day_of_week, road_type, weather_condition):
    input_data = pd.DataFrame([{
        "Hour": hour,
        "Day_of_Week": day_of_week,
        "Road_Type": road_type,
        "Weather_Condition": weather_condition
    }])
    prediction = model.predict(input_data)[0]
    probs = model.predict_proba(input_data)[0]
    classes = model.classes_
    prob_dict = dict(zip(classes, probs))
    return prediction, prob_dict
