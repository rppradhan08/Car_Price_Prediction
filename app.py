import pickle
from flask import Flask, render_template, request, redirect, jsonify
import requests
import numpy as np
import sklearn


app = Flask(__name__)

# Loading model
model = pickle.load(open("Linear_regressor.pkl", "rb"))

def parseRequest(result):
    '''
    Function for parsing request made to server by client.
    '''
    Present_Price = float(result['Present_Price'])
    Kms_Driven = int(result['Kms_Driven'])
    Owner = int(result['Owner'])
    Age = int(result['Age'])
    Fuel_Type = result['Fuel_Type']
    if(Fuel_Type == 'Petrol'):
        Fuel_Type_Petrol = 1
        Fuel_Type_Diesel = 0
    else:
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 1
    Seller_Type = result['Seller_Type']
    if(Seller_Type == 'Individual'):
        Seller_Type_Individual = 1
    else:
        Seller_Type_Individual = 0
    Transmission = result['Transmission']
    if(Transmission == 'Manual'):
        Transmission_Manual = 1
    else:
        Transmission_Manual = 0
    return [[Present_Price, Kms_Driven, Owner, Age, Fuel_Type_Diesel,
                Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]]

def getPrediction(result):
    '''
    Function for performing prediction using imported model
    '''
    formatted_result = parseRequest(result)
    prediction = model.predict(formatted_result)
    return round(prediction[0], 2)

@app.route('/', methods=['GET'])
def Home():
    '''
    Home End-point
    '''
    return render_template('index.html')

@app.route("/predict", methods=['POST','GET'])
def predict():
    '''
    Receives Forms and JSON 
    '''
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        # Accessing content of form using there name attribute
        content_type = request.headers.get('Content-Type')
        if request.form:
            # request revieved via form
            result = {}
            for key, value in request.form.to_dict(flat=False).items():
               result[key] = value[0] if len(value) == 1 else value
            output = getPrediction(result)
            if output < 0:
                return render_template('result.html', prediction_text="<h2>Sorry you cannot sell this car</h2>")
            else:
                return render_template('result.html', prediction_text="You can sell the car at {} Lacs".format(output))

        elif request.get_json(force=True):
            # request revieved in JSON format
            result = request.get_json(force=True)
            output = getPrediction(result)
            return jsonify(output)

        else: 
            # This will get executed if /predict endpoint is hit with any method except POST
            return render_template('index.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


# Handling requests in flask
# Ref-1: https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# Ref-2: https://stackoverflow.com/questions/10999990/get-raw-post-body-in-python-flask-regardless-of-content-type-header

'''
Sample JSON input.
{
    "Present_Price": 10,
    "Kms_Driven": 100000,
    "Owner": 1,
    "Age": 2,
    "Fuel_Type": "Petrol",
    "Seller_Type": "Individual",
    "Transmission": "Manual"

'''