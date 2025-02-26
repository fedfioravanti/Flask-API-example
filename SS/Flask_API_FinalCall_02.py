from flask import Flask, request, jsonify
import joblib
import traceback
import numpy as np
import pandas as pd

app = Flask(__name__)

# load the model (do this ONCE when the app starts)
model_path = 'D:/Federico/02_Projects/01_Data_Science/07_Flask-API-example/models/FinalCall-GBC-01.pkl'
try:
    model = joblib.load(model_path)
    print('Model loaded!')
except Exception as e:
    print(f"Error loading model: {e}")
    exit()


@app.route('/', methods=['GET'])
def pri():
    return f"welcome"

    
@app.route('/predict', methods=['GET'])
def predict():
    if model:
        try:
            json_ = request.json
            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))
            # query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(model.predict(query))

            return jsonify({'prediction': str(prediction)})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

if __name__ == '__main__':
    # app.run(debug=True) 
    predict()