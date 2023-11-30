import json
from io import StringIO

import pandas as pd
from flask import Flask, request, Response
from flask_cors import CORS
from waitress import serve

TEXT_CSV = 'text/csv'

app = Flask(__name__)
cors = CORS(app)


@app.route('/subtract', methods=['POST'])
def request_txt():
    percent = abs(float(request.headers['percent'])) / 100
    json_data = json.loads(request.data)
    component_io = StringIO(json_data['subtract_component'])
    component_df = pd.read_csv(component_io, sep=",", header=None)
    samples_io = StringIO(json_data['samples'])
    samples_df = pd.read_csv(samples_io, sep=",", header=None)
    component_df = component_df.drop([0], axis=1)
    sample_names_df = pd.DataFrame(samples_df[0])
    sample_names_df[0] = sample_names_df[0] + '_sub'
    samples_df = samples_df.drop([0], axis=1)
    calculated_df = pd.DataFrame((samples_df.values - percent * component_df.values[0]) / (1 - percent))
    result_df = pd.concat([sample_names_df, calculated_df], axis=1)
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


if __name__ == '__main__':
    print('auCalculator ready!')
    serve(app,
          host='0.0.0.0',
          port=8080)
