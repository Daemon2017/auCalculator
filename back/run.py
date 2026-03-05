import json
from itertools import combinations

import pandas as pd
from flask import Flask, request, Response
from flask_cors import CORS
from waitress import serve

import utils

TEXT_CSV = 'text/csv'

app = Flask(__name__)
cors = CORS(app)


def apply_prefix(df, prefix):
    if prefix:
        df[0] = prefix + df[0].astype(str)
    return df


@app.route('/subtract', methods=['POST'])
def subtract():
    json_data = json.loads(request.data)
    component_names_df, component_data_df = utils.get_names_data_df(json_data['component'])
    samples_names_df, samples_data_df = utils.get_names_data_df(json_data['samples'])
    samples_names_df[0] = samples_names_df[0].str.replace(r'^([^:]+)', r'\1_sub', regex=True)
    percent = abs(float(request.headers['percent'])) / 100
    calculated_data_df = pd.DataFrame((samples_data_df.values - percent * component_data_df.values[0]) / (1 - percent))
    result_df = pd.concat([samples_names_df, calculated_data_df], axis=1)
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/add', methods=['POST'])
def add():
    json_data = json.loads(request.data)
    component_names_df, component_data_df = utils.get_names_data_df(json_data['component'])
    samples_names_df, samples_data_df = utils.get_names_data_df(json_data['samples'])
    samples_names_df[0] = samples_names_df[0].str.replace(r'^([^:]+)', r'\1_add', regex=True)
    percent = abs(float(request.headers['percent'])) / 100
    calculated_data_df = pd.DataFrame((samples_data_df.values + percent * component_data_df.values[0]) / (1 + percent))
    result_df = pd.concat([samples_names_df, calculated_data_df], axis=1)
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/average', methods=['POST'])
def total_average():
    json_data = json.loads(request.data)
    samples_names_df, samples_data_df = utils.get_names_data_df(json_data['samples'])
    result_df = pd.DataFrame([samples_data_df.mean(axis=0)])
    result_df.insert(loc=0, column=0, value='average')
    result_df = apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/pair', methods=['POST'])
def pair_average():
    json_data = json.loads(request.data)
    names_df, data_df = utils.get_names_data_df(json_data['samples'])

    pairs_list = []
    for i, j in combinations(range(len(names_df)), 2):
        combined_name = f"{names_df.iloc[i, 0]}_{names_df.iloc[j, 0]}"
        avg_coords = (data_df.iloc[i] + data_df.iloc[j]) / 2
        res_row = [combined_name] + avg_coords.tolist()
        pairs_list.append(res_row)

    result_df = pd.DataFrame(pairs_list)
    result_df = apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/group', methods=['POST'])
def group_average():
    json_data = json.loads(request.data)
    fathers_names, fathers_data = utils.get_names_data_df(json_data['component'])
    mothers_names, mothers_data = utils.get_names_data_df(json_data['samples'])

    results = []
    for i in range(len(fathers_names)):
        for j in range(len(mothers_names)):
            combined_name = f"{fathers_names.iloc[i, 0]}_{mothers_names.iloc[j, 0]}"
            avg_coords = (fathers_data.iloc[i] + mothers_data.iloc[j]) / 2
            results.append([combined_name] + avg_coords.tolist())

    result_df = pd.DataFrame(results)
    result_df = apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


if __name__ == '__main__':
    print('auCalculator ready!')
    serve(app,
          host='0.0.0.0',
          port=8080)
