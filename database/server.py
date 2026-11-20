from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# ======================
# DATABASE CONNECTION
# ======================

conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_YPutR6wViH3L@ep-square-star-be6fg2ub-pooler.c-9.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

cur = conn.cursor()



conn.commit()
cur.close()


# ======================
# ANOMALY DETECTION
# ======================

def detect_status(flow, pressure, vibration):

    if flow is None:
        return "Flow Sensor Failure"

    if pressure is None:
        return "Pressure Sensor Failure"

    if vibration is None:
        return "Vibration Sensor Failure"

    if flow < 0:
        return "Flow Sensor Error"

    if pressure < 0:
        return "Pressure Sensor Error"

    if vibration < 0:
        return "Vibration Sensor Error"

    return "Monitoring"


# ======================
# HOME PAGE
# ======================

@app.route("/")
def home():

    return "Server Working"


# ======================
# GET LATEST DATA
# ======================

@app.route("/data", methods=["GET"])
def get_data():

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            flow_rate,
            pressure,
            vibration,
            status,
            created_at
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cur.fetchall()

    cur.close()

    return jsonify(rows)


# ======================
# ESP32 SENSOR ENDPOINT
# ======================

@app.route("/sensor", methods=["POST"])
def sensor():

    try:

        data = request.json

        flow_rate = data["flow_rate"]

        pressure = data.get(
            "pressure",
            0
        )

        vibration = data.get(
            "vibration",
            0
        )

        status = detect_status(
            flow_rate,
            pressure,
            vibration
        )

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO sensor_data
            (
                flow_rate,
                pressure,
                vibration,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                flow_rate,
                pressure,
                vibration,
                status
            )
        )

        conn.commit()

        cur.close()

        return jsonify(
            {
                "success": True,
                "status": status
            }
        )

    except Exception as e:

        return jsonify(
            {
                "success": False,
                "status": "Database Failure",
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