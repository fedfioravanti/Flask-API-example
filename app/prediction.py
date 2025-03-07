# Import dependencies
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
import json

# prediction definition
def predict_BMI_status(config):
    # load the model from the saved file
    pkl_filename = "../model.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = joblib.load(f_in)

    scaler = StandardScaler()

    if type(config) == dict:
        df = pd.DataFrame(config)
        # df.iloc[:,:] = scaler.transform(df.iloc[:,:])
    else:
        df = config
    
    pred_test = model.predict(df)
    
    if pred_test == 0:
        return 'Severe Obese'
    elif pred_test == 1:
        return 'Obese'
    elif pred_test == 2:
        return 'Overweight'
    elif pred_test == 3:
        return 'Normal'
    elif pred_test == 4:
        return 'Mild Thinness'
    elif pred_test == 5:
        return 'Moderate Thinness'
    elif pred_test == 6:
        return 'Severe Thinness'
