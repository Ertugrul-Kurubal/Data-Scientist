import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import sys
import logging

app = Flask(__name__, template_folder='templates')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
loaded_model = pickle.load(open("rf_final_model.pkl", "rb"))
loaded_scaler = pickle.load(open("scaler.pkl", "rb"))
loaded_columns = pickle.load(open("Xcolums.pkl", "rb"))


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    print('Enter input values')
    my_dict = [float(x) for x in request.form.values()]
    my_dict = pd.DataFrame([my_dict], columns=loaded_columns)
    my_dict = loaded_scaler.transform(my_dict)
    result = loaded_model.predict(my_dict)
    prediction = loaded_model.predict_proba(my_dict)
    output = prediction[0][1]
    print(result)
    if output > 0.50:
        return render_template('index.html', prediction_text=f'{result} ATTENTION PLEASE !!! THE TRANSACTION IS {output} LIKELY FRADULENT.')
    elif output <= 0.50:
        return render_template('index.html', prediction_text=f'{result} EVERYTHING SEEMS OKAY... THE TRANSACTION IS {output} LIKELY NON-FRADULENT.')
    else:
        return render_template('index.html', prediction_text='PLEASE ENTER THE CORRECT VALUES IN THE FIELDS TO PREDICT THE FRAUD OF THE TRANSACTION.') 

if __name__ == "__main__":
    # app.run(debug=True) # Local host bağlantı için bu kod kullanılmalı
    app.run(debug=True, port=80, host="0.0.0.0") # External (http) bağlantılar için bu kod kullanılmalı

