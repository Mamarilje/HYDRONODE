import pandas as pd
import joblib

# Load models
status_model = joblib.load("status_model.pkl")
location_model = joblib.load("location_model.pkl")

sample_data = pd.DataFrame(
    [[
        4.8, 4.7, 4.6, 4.5,
        2400, 2380, 2360, 2340
    ]],
    columns=[
        "flow1",
        "flow2",
        "flow3",
        "flow4",
        "pressure1",
        "pressure2",
        "pressure3",
        "pressure4"
    ]
)

status_prediction = status_model.predict(sample_data)
status_confidence = status_model.predict_proba(sample_data)

location_prediction = location_model.predict(sample_data)
location_confidence = location_model.predict_proba(sample_data)

print("Status:")
print(status_prediction[0])

print(
    "Status Confidence:",
    round(max(status_confidence[0]) * 100, 2),
    "%"
)

print()

print("Localization:")
print(location_prediction[0])

print(
    "Localization Confidence:",
    round(max(location_confidence[0]) * 100, 2),
    "%"
)