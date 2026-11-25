import pandas as pd
import random

data = []

# 50 NORMAL
for _ in range(50):
    data.append([
        random.randint(280,320),
        random.randint(280,320),
        random.randint(280,320),
        random.randint(280,320),

        random.randint(42,48),
        random.randint(42,48),
        random.randint(42,48),
        random.randint(42,48),

        "Normal",
        "None"
    ])

# 50 ZONE1 LEAK
for _ in range(50):
    data.append([
        random.randint(280,320),
        random.randint(120,180),
        random.randint(110,170),
        random.randint(100,160),

        random.randint(42,48),
        random.randint(15,25),
        random.randint(15,25),
        random.randint(15,25),

        "Leak",
        "Zone1"
    ])

# 50 ZONE2 LEAK
for _ in range(50):
    data.append([
        random.randint(280,320),
        random.randint(280,320),
        random.randint(120,180),
        random.randint(100,160),

        random.randint(42,48),
        random.randint(42,48),
        random.randint(15,25),
        random.randint(15,25),

        "Leak",
        "Zone2"
    ])

# 50 ZONE3 LEAK
for _ in range(50):
    data.append([
        random.randint(280,320),
        random.randint(280,320),
        random.randint(280,320),
        random.randint(120,180),

        random.randint(42,48),
        random.randint(42,48),
        random.randint(42,48),
        random.randint(15,25),

        "Leak",
        "Zone3"
    ])

# 50 SENSOR FAILURE
for _ in range(50):
    data.append([
        0,0,0,0,
        0,0,0,0,
        "SensorFailure",
        "None"
    ])

df = pd.DataFrame(
    data,
    columns=[
        "flow1",
        "flow2",
        "flow3",
        "flow4",
        "pressure1",
        "pressure2",
        "pressure3",
        "pressure4",
        "status",
        "localization"
    ]
)

df.to_csv(
    "train_data.csv",
    index=False
)

print("250 rows generated!")