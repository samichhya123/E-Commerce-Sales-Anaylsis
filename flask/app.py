import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd


app = Flask(__name__)


# Load the trained model
sales_model = pickle.load(open('models/sales_analysis_model.pkl', 'rb'))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        # Retrieve features from the form in index.html
        sku_code = int(request.form.get('SKU Code'))
        design_no = int(request.form.get('Design No.'))
        category = int(request.form.get('Category'))
        size = int(request.form.get('Size'))
        color = int(request.form.get('Color'))
        
        # Create a DataFrame from the inputs to match model training data
        input_data = pd.DataFrame([[sku_code, design_no, category, size, color]],
                                  columns=['SKU Code', 'Design No.', 'Category', 'Size', 'Color'])

        # Predict using the loaded model
        prediction = sales_model.predict(input_data)
        
        # Return the prediction result to the user
        return render_template('predict.html', outcome=round(prediction[0], 2))
    else:
        return render_template('predict.html')

if __name__ == "__main__":
    app.run(debug=True)
