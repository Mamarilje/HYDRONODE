from flask import Flask, request, jsonify
import psycopg2
import pandas as pd
import joblib
import traceback

app = Flask(__name__)

# ======================
# DATABASE CONNECTION
# ======================

conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_YPutR6wViH3L@ep-square-star-be6fg2ub-pooler.c-9.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

# ======================
# LOAD ML MODELS
# ======================

status_model = joblib.load("status_model.pkl")
location_model = joblib.load("location_model.pkl")

# ======================
# HOME PAGE
# ======================

@app.route("/")
def home():
    return "HydroNode Server Running"

# ======================
# GET DATA
# ======================

@app.route("/data", methods=["GET"])
def get_data():

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            created_at,
            status,
            flow1,
            flow2,
            flow3,
            flow4,
            pressure1,
            pressure2,
            pressure3,
            pressure4,
            localization,
            confidence,
            pump_status
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 50
    """)

    rows = cur.fetchall()

    cur.close()

    return jsonify(rows)

# ======================
# SENSOR ENDPOINT
# ======================

@app.route("/sensor", methods=["POST"])
def sensor():

    try:

        data = request.json

        flow1 = float(data["flow1"])
        flow2 = float(data["flow2"])
        flow3 = float(data["flow3"])
        flow4 = float(data["flow4"])

        pressure1 = float(data["pressure1"])
        pressure2 = float(data["pressure2"])
        pressure3 = float(data["pressure3"])
        pressure4 = float(data["pressure4"])

        pump_status = data.get(
            "pump_status",
            "OFF"
        )

        sample = pd.DataFrame(
            [[
                flow1,
                flow2,
                flow3,
                flow4,
                pressure1,
                pressure2,
                pressure3,
                pressure4
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

        # Predict Status

        status = status_model.predict(sample)[0]

        confidence = float(
    round(
        max(
            status_model.predict_proba(sample)[0]
        ) * 100,
        2
    )
)   

        # Predict Location

        localization = "None"

        if status == "Leak":
            localization = location_model.predict(sample)[0]

        # Save to Database

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO sensor_data
            (
                status,
                flow1,
                flow2,
                flow3,
                flow4,
                pressure1,
                pressure2,
                pressure3,
                pressure4,
                localization,
                confidence,
                pump_status
            )
            VALUES
            (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s
            )
            """,
            (
                status,
                flow1,
                flow2,
                flow3,
                flow4,
                pressure1,
                pressure2,
                pressure3,
                pressure4,
                localization,
                confidence,
                pump_status
            )
        )

        conn.commit()

        cur.close()

        return jsonify(
            {
                "success": True,
                "status": status,
                "localization": localization,
                "confidence": confidence,
                "pump_status": pump_status
            }
        )

    except Exception as e:

        print("\n====================")
        print("SERVER ERROR")
        print("====================")
        traceback.print_exc()
        print("====================\n")

        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500

# ======================
# RUN SERVER
# ======================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )