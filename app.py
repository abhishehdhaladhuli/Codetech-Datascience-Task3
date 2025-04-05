from flask import Flask, request, render_template
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

model = joblib.load("model/trained_model.pkl")
label_encoders = joblib.load("model/label_encoders.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            input_data = {
                "Company": request.form["company"],
                "TypeName": request.form["typename"],
                "Inches": float(request.form["inches"]),
                "ScreenResolution": request.form["screenresolution"],
                "Cpu": request.form["cpu"],
                "Ram": int(request.form["ram"]),
                "Memory": request.form["memory"],
                "Gpu": request.form["gpu"],
                "OpSys": request.form["opsys"],
                "Weight": float(request.form["weight"])
            }

            df = pd.DataFrame([input_data])

            for col in df.columns:
                if col in label_encoders:
                    df[col] = label_encoders[col].transform(df[col])

            pred = model.predict(df)[0]
            prediction = round(pred, 2)
        except Exception as e:
            error = str(e)

    return render_template("index.html", prediction=prediction, error=error)

if __name__ == "__main__":
    app.run(debug=True)
