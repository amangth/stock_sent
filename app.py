# from flask import Flask, render_template, request
# import pickle
# import pandas as pd
# from flask_cors import cross_origin

# app = Flask(__name__)

# model = pickle.load(open('stocksent.plk', 'rb'))

# @app.route("/")
# @cross_origin()
# def home():
#     return render_template("index.html")




# @app.route("/predict", methods = ["GET", "POST"])
# @cross_origin()

# def prepare_data(input):
#     input_data = pd.DataFrame([input], columns=['Close','Volume', 'Open', 'High', 'Title'])
#     return input_data

# @app.route('/', methods=['GET', 'POST'])
# def predict(input_data):
#     if request.method == 'POST':
#         close = request.form['Close']
#         volume= request.form['volume']
#         open_price = request.form['Open']
#         high_price = request.form['High']
#         title = request.form['Title']

#         input_data = prepare_data({'Close': close,'Volume':volume, 'Open': open_price, 'High': high_price, 'Title': title})
#         prediction = model.predict(input_data)
#         output = round(prediction[0], 2)

#         return render_template('index.html', prediction_text="The prediction for {} is ${}".format(title, output))

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

import pickle
import pandas as pd
from flask import Flask, render_template, request
from flask_cors import cross_origin

app = Flask(__name__)

model = pickle.load(open('stocksent.plk', 'rb'))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

def prepare_data(input):
    input_data = pd.DataFrame([input], columns=['Volume_data', 'Open_data', 'Close_data', 'polarity_data', 'Actual_Close'])
    for column in input_data.columns:
        input_data[column] = pd.to_numeric(input_data[column], errors='coerce')
    return input_data

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        close_data = request.form['Close_data']
        volume_data= request.form['Volume_data']
        open_data = request.form['Open_data']
        actual_Close = request.form['Actual_Close']
        polarity_data = request.form['polarity_data']
        input_data = prepare_data({'Close_data': close_data,'Volume_data':volume_data, 'Open_data': open_data, 'Actual_Close': actual_Close, 'polarity_data': polarity_data})
        prediction = model.predict(input_data)
        output = round(prediction[0], 2)

        return render_template('index.html', prediction_text="The prediction (1 for rise from current level, 0 for drop)for TSLA is {}".format(output))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)