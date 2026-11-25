import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("train_data.csv")

df["localization"] = df["localization"].fillna("NONE")

X = df[
    [
        "flow1",
        "flow2",
        "flow3",
        "flow4",
        "pressure1",
        "pressure2",
        "pressure3",
        "pressure4"
    ]
]

y = df["localization"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "location_model.pkl"
)

print("Localization model trained!")