from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# load the model (do this ONCE when the app starts)
model_path = 'D:/Federico/02_Projects/01_Data_Science/07_Flask-API-example/models/FinalCall-GBC-01.pkl'
try:
    model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    exit()


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # get input data from the request
        data = request.get_json()

        if data is None:
            return jsonify({'error': 'No input data provided'}), 400

        # Example: if you expect a single feature
        # feature = data['feature']
        # input_data = np.array([[feature]]) # Reshape as needed for your model

        # Example: If you expect multiple features, you might have
        # input_data = np.array([data['features']])

        # Example: If you expect a csv file
        # file = request.files['file']
        # df = pd.read_csv(file)
        # input_data = df.values

        # 2. Preprocess Input (if necessary)
        # This step is CRUCIAL.  Make sure your preprocessing here
        # EXACTLY matches the preprocessing you did during training.
        # This might include scaling, one-hot encoding, etc.

        # make prediction
        try:
            prediction = model.predict(input_data)
        except Exception as e:
            return jsonify({'error': f'Prediction error: {e}'}), 500

        # format the response
        if isinstance(prediction, np.ndarray):
            prediction = prediction.tolist()
        elif isinstance(prediction, pd.DataFrame):
            prediction = prediction.values.tolist()
        
        output = {'prediction': prediction} 

        return jsonify(output), 200 

    except Exception as e:
        return jsonify({'error': str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)  
