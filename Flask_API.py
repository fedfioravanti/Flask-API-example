import joblib

def load_model(model_path):
    model = joblib.load(model_path) # Load the model
    return model


from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the model (do this ONCE when the app starts)
model = load_model('my_model.pkl') # Or the path to your model file

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Get Input Data from the Request
        data = request.get_json()  # Assumes JSON input

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

        # 3. Make Prediction
        prediction = model.predict(input_data)

        # 4. Format the Response
        # Convert predictions to a JSON-serializable format
        output = {'prediction': prediction.tolist()} # .tolist() if it is a numpy array

        return jsonify(output), 200  # 200 OK

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 500 Internal Server Error

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production
