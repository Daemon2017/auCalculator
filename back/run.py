import json
from itertools import combinations

import pandas as pd
from flask import Flask, request, Response
from flask_cors import CORS
from sklearn.decomposition import PCA
from waitress import serve

import utils

TEXT_CSV = 'text/csv'

app = Flask(__name__)
cors = CORS(app)


@app.route('/subtract', methods=['POST'])
def subtract():
    json_data = json.loads(request.data)
    component_names_df, component_data_df = utils.get_names_data_df(json_data['component'])
    samples_names_df, samples_data_df = utils.get_names_data_df(json_data['samples'])
    percent = abs(float(request.headers['percent'])) / 100
    results = []
    for i in range(len(samples_names_df)):
        for j in range(len(component_names_df)):
            combined_name = f"{samples_names_df.iloc[i, 0]}_minus_{component_names_df.iloc[j, 0]}"
            calc_coords = (samples_data_df.iloc[i] - percent * component_data_df.iloc[j]) / (1 - percent)
            results.append([combined_name] + calc_coords.tolist())
    result_df = pd.DataFrame(results)
    result_df = utils.apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/add', methods=['POST'])
def add():
    json_data = json.loads(request.data)
    component_names_df, component_data_df = utils.get_names_data_df(json_data['component'])
    samples_names_df, samples_data_df = utils.get_names_data_df(json_data['samples'])
    percent = abs(float(request.headers['percent'])) / 100
    results = []
    for i in range(len(samples_names_df)):
        for j in range(len(component_names_df)):
            combined_name = f"{samples_names_df.iloc[i, 0]}_plus_{component_names_df.iloc[j, 0]}"
            calc_coords = (samples_data_df.iloc[i] + percent * component_data_df.iloc[j]) / (1 + percent)
            results.append([combined_name] + calc_coords.tolist())
    result_df = pd.DataFrame(results)
    result_df = utils.apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/reconstruct', methods=['POST'])
def reconstruct_ancestral():
    json_data = json.loads(request.data)
    samples_names_df, samples_data_df = utils.get_names_data_df(json_data['samples'])
    pca = PCA(n_components=1)
    transformed = pca.fit_transform(samples_data_df.values)
    reconstructed_vector = pca.inverse_transform(transformed)
    ancestral_coords = reconstructed_vector.mean(axis=0)
    results = [["reconstructed"] + ancestral_coords.tolist()]
    result_df = pd.DataFrame(results)
    result_df = utils.apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/total_average', methods=['POST'])
def total_average():
    json_data = json.loads(request.data)
    samples_names_df, samples_data_df = utils.get_names_data_df(json_data['samples'])
    result_df = pd.DataFrame([samples_data_df.mean(axis=0)])
    result_df.insert(loc=0, column=0, value='average')
    result_df = utils.apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/pair_average', methods=['POST'])
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
    result_df = utils.apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


@app.route('/group_average', methods=['POST'])
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
    result_df = utils.apply_prefix(result_df, request.headers.get('prefix'))
    return Response(result_df.to_csv(sep=',', index=False, header=False), mimetype=TEXT_CSV)


if __name__ == '__main__':
    print('auCalculator ready!')
    serve(app,
          host='0.0.0.0',
          port=8080)
