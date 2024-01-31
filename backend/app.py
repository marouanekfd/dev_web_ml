from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
from matplotlib import pyplot as plt
import pkg_resources
import os
import pandas as pds
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

devmode = True
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
    df = pds.read_csv(file_path)
    json_data = df.to_json(orient='records')
    columns_list = df.columns.tolist()
    return jsonify({'success': 'File successfully uploaded', 'data': columns_list})

@app.route('/api/predire', methods=['POST'])
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

@app.route('/api/visualisation', methods=['POST'])
def vizu():
    upload_folder = '../data'
    file = request.files['file']
    file_path = os.path.join(upload_folder, file.filename)
    df = pds.read_csv(file_path)
    fig = plt.figure(figsize=(10, 8))
    sns.pairplot(df)
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')
if __name__ == '__main__':
    app.run(port=4000,debug=devmode)