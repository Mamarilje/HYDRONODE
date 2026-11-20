import pandas as pd
import joblib

model = joblib.load("model.pkl")

sample_data = pd.DataFrame(
    [[140, 23, 0.12]],
    columns=[
        "flow_rate",
        "pressure",
        "vibration"
    ]
)

prediction = model.predict(sample_data)

confidence = model.predict_proba(sample_data)

print("Prediction:", prediction[0])

print(
    "Confidence:",
    round(max(confidence[0]) * 100, 2),
    "%"
)