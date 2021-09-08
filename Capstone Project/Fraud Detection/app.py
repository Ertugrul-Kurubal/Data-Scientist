import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import sys
import logging



# @app.route("/api", methods = ["GET", "POST"])
# def home():
#     if request.method == "POST":
#         my_dict = {
#             "time": request.form["time"],
#             "v1": request.form["v1"],
#             "v2": request.form["v2"],
#             "v3": request.form["v3"],
#             "v4": request.form["v4"],
#             "v5": request.form["v5"],
#             "v6": request.form["v6"],
#             "v7": request.form["v7"],
#             "v8": request.form["v8"],
#             "v9": request.form["v9"],
#             "v10": request.form["v10"],
#             "v11": request.form["v11"],
#             "v12": request.form["v12"],
#             "v13": request.form["v13"],
#             "v14": request.form["v14"],
#             "v15": request.form["v15"],
#             "v16": request.form["v16"],
#             "v17": request.form["v17"],
#             "v18": request.form["v18"],
#             "v19": request.form["v19"],
#             "v20": request.form["v20"],
#             "v21": request.form["v21"],
#             "v22": request.form["v22"],
#             "v23": request.form["v23"],
#             "v24": request.form["v24"],
#             "v25": request.form["v25"],
#             "v26": request.form["v26"],
#             "v27": request.form["v27"],
#             "v28": request.form["v28"],
#             "amount": request.form["amount"]
#             }
#         my_dict = pd.DataFrame([my_dict], columns=loaded_columns)
#         my_dict = loaded_scaler.transform(my_dict)
#         result = loaded_model.predict(my_dict)
#         return {"predicted price:":str(result)}
#     else:
#         return "get method"

app = Flask(__name__, template_folder='templates')

@app.route("/", methods = ["GET", "POST"])

def home():
    if request.method == "POST":
        my_dict = {
            "time": request.form["time"],
            "v1": request.form["v1"],
            "v2": request.form["v2"],
            "v3": request.form["v3"],
            "v4": request.form["v4"],
            "v5": request.form["v5"],
            "v6": request.form["v6"],
            "v7": request.form["v7"],
            "v8": request.form["v8"],
            "v9": request.form["v9"],
            "v10": request.form["v10"],
            "v11": request.form["v11"],
            "v12": request.form["v12"],
            "v13": request.form["v13"],
            "v14": request.form["v14"],
            "v15": request.form["v15"],
            "v16": request.form["v16"],
            "v17": request.form["v17"],
            "v18": request.form["v18"],
            "v19": request.form["v19"],
            "v20": request.form["v20"],
            "v21": request.form["v21"],
            "v22": request.form["v22"],
            "v23": request.form["v23"],
            "v24": request.form["v24"],
            "v25": request.form["v25"],
            "v26": request.form["v26"],
            "v27": request.form["v27"],
            "v28": request.form["v28"],
            "amount": request.form["amount"]
            }
        my_dict = pd.DataFrame([my_dict], columns=loaded_columns)
        my_dict = loaded_scaler.transform(my_dict)
        result = loaded_model.predict(my_dict)
        return render_template("index.html", result = f"$ {result[0]:,.2f}" )
    else:
        return render_template("index.html")
    
if __name__ == "__main__":
    
    loaded_model = pickle.load(open("rf_final_model.pkl", "rb"))
    loaded_scaler = pickle.load(open("scaler.pkl", "rb"))
    loaded_columns = pickle.load(open("Xcolums.pkl", "rb"))

    app.run(debug=True, port=80, host="0.0.0.0")