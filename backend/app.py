from flask import Flask, render_template, request, jsonify
import pkg_resources
import os
import pandas as pds
import csv

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


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
    
app = Flask(_name_,
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

@app.route('/api/train-random-forest', methods=['POST'])
def predict():
    upload_folder = '../data'
    file = request.form['file']

    target = request.form['target']
    file_path = os.path.join(upload_folder, file)
    df = pds.read_csv(file_path)
    X=df.drop(columns={target})
    y=df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    clf=RandomForestClassifier(n_estimators=100)
    clf.fit(X_train,y_train)

    y_pred=clf.predict(X_test)
    return jsonify({'success': 'model success', 'data': metrics.accuracy_score(y_test, y_pred)})


@app.route('/api/submit-kmeans-params', methods=['POST'])
def handle_kmeans_params():
    # Algorithme machine learning
    data = request.json
    print(data)
    i = data['params']['init']
    m = data['params']['max_iter']
    k = data['params']['n_clusters']
    t = data['params']['tol']

    iris_data = pds.read_csv('/Users/gabrielpapalia/Desktop/Cours/MASTER IDA/M2 /Untitled Folder/templateFlaskVue/data/iris.csv', sep = ";")

    # Préparer les données pour l'entraînement
    # Supposons que les quatre premières colonnes sont des caractéristiques
    X = iris_data.iloc[:, :-1]

    # Normalisation des caractéristiques
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Entraînement de KMeans
    kmeans = KMeans(n_clusters=k, random_state=42, init =i, max_iter =m,tol = t) 
    kmeans.fit(X_scaled)

    # Prédiction des clusters
    labels = kmeans.labels_

    # Évaluation avec le score silhouette
    silhouette = silhouette_score(X_scaled, labels)

    #print("Score silhouette:", silhouette)
    return jsonify(silhouette)


    #return jsonify({"status": "Reçu et renvoyé", "data": data})

if _name_ == '_main_':
    app.run(port=4000,debug=devmode)