import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("train_data.csv")

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

y = df["status"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "status_model.pkl"
)

print("Status model trained!")