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
    json_data = json.loads(request.data)
    component_names_df, component_data_df = get_names_data_df(json_data['component'])
    samples_names_df, samples_data_df = get_names_data_df(json_data['samples'])
    samples_names_df[0] = samples_names_df[0].str.replace(r'^([^:]+)', r'\1_sub', regex=True)
    percent = abs(float(request.headers['percent'])) / 100
    calculated_data_df = pd.DataFrame((samples_data_df.values - percent * component_data_df.values[0]) / (1 - percent))
    result_df = pd.concat([samples_names_df, calculated_data_df], axis=1)
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


def get_names_data_df(data):
    data_io = StringIO(data)
    data_df = pd.read_csv(data_io, sep=",", header=None)
    names_df = pd.DataFrame(data_df[0])
    data_df = data_df.drop([0], axis=1)
    return names_df, data_df


if __name__ == '__main__':
    print('auCalculator ready!')
    serve(app,
          host='0.0.0.0',
          port=8080)
