from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import securefilename
import os
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Dict
import pathlib
import pandas as pd
import openai
import script
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)  # This will enable CORS for all routes
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

filenames = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('files[]')

    if not files or files[0].filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if len(files) > 10:
        return jsonify({'error': 'Cannot upload more than 10 files'}), 400


    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            filenames.append(filename)
        else:
            return jsonify({'error': 'Invalid file format. Only JPEG images are allowed.'}), 400

    return jsonify({'message': 'Files successfully uploaded', 'filenames': filenames}), 200




@app.route('/score', methods=['POST'])
def get_score():
    data = request.get_json()
    if 'location' in data and 'k' in data: 
        location = data['location']
        k_value = data['k']
        nearest_k = script.return_nearest_scores(location, k_value)
        nearest_k_dict = nearest_k.to_dict(orient='records')
        return jsonify(nearest_k_dict)

    return jsonify({'status_code': 400})




main_api_key = "gt51b6ea"


# Functions (get_file_type, post_files, delete_files, summarize, describe) defined in scripy.py

@app.route('/positivity-score', methods=['POST'])
def get_positivity_score():
    return script.score_positivity_helper(filenames)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/test')
def hello_world():
    return 'Hello World'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')
