from flask import Flask, render_template, request, jsonify
import pkg_resources
import os
import pandas as pds
import csv
import saving_models
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import pickle

devmode = True
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_delimiter(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        sample = file.read(4096)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)

        return dialect.delimiter
    
app = Flask(__name__,
        static_folder = "../frontend/dist/assets",
        template_folder = "../frontend/dist")



@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/api/python_pkg')
def pkg():
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s  %s" % (i.key, i.version) for i in installed_packages])
    return installed_packages_list


@app.route('/api/mode')
def getMode():
    return {"devmode":devmode}

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed file types: csv'})

    upload_folder = '../data'

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    delimiter = detect_delimiter(file_path)

    df = pds.read_csv(file_path, sep=delimiter)
    json_data = df.to_json(orient='records')
    columns_list = df.columns.tolist()
    return jsonify({'success': 'File successfully uploaded', 'data': columns_list})

@app.route('/api/train', methods=['POST'])
def train():
    data = request.json
    target = data.get('target')
    n_estimators = data['params'].get('n_estimators')
    max_depth = data['params'].get('max_depth')
    random_state = data['params'].get('random_state')
    min_samples_split = data['params'].get('min_samples_split')
    dataset_name = data.get('filename')
    split = data['split'].get('train_size') / 100
    
    try:
        dataset = pds.read_csv(f'../data/{dataset_name}', sep=",")
    except FileNotFoundError:
        return jsonify({"error": "Fichier non trouvé"}), 402
    X = dataset.drop(target, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, dataset[target], train_size=split, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    try:
        if(data['params'].get('model') == 'RandomForestClassifier'):
            rf = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
                min_samples_split=min_samples_split
            )
        else:
            rf = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
                min_samples_split=min_samples_split
            )
        rf.fit(X_train_scaled, y_train)
    except Exception as e:
        return jsonify({"error": "Veuillez choisir un autre modèle"}), 500
    y_pred_test = rf.predict(X_test_scaled)
    y_pred_train = rf.predict(X_train_scaled)

    accuracy_test = accuracy_score(y_test, y_pred_test)
    accuracy_train = accuracy_score(y_train, y_pred_train)

    token = saving_models.generate_token()

    saving_models.save_model(rf, dataset_name, token, target)
    return jsonify({"accuracy_test": accuracy_test,'accuracy_train': accuracy_train, "token": token})

@app.route('/api/data', methods=['POST'])

def data():
    values_data = request.form['values']
    return jsonify({ "values": values_data, 'values_data': values_data})


@app.route('/api/predict', methods=['POST'])
def predict():
    token = request.form['token']
    data = request.form['values']
    filename = os.path.join('saved_models', f'model_{token}.pkl')
    with open(filename, 'rb') as file:
        model_info = pickle.load(file)
    df = pds.read_json(data, orient='index')
    df = df.T
    prediction = model_info['model'].predict(df.iloc[0:1, :])
    return jsonify({"prediction": prediction[0]})



@app.route('/api/delete-model', methods=['POST'])
def delete_model():
    data = request.json
    return saving_models.delete_model(data['token'])


@app.route('/api/data-files', methods=['POST'])
def list_data_files():
    data_directory = '../data'
    try:
        files = [f for f in os.listdir(data_directory) if os.path.isfile(os.path.join(data_directory, f))]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(port=4000,debug=devmode)