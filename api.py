from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import script
from script import post_files, summarize, get_summarized_test, summarize_files_and_get_insights, analyze_sentiment_and_get_score


app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)  # This will enable CORS for all routes

file_ids = []
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

#app = Flask(__name__)

# Assuming you have a directory named 'uploads' in the same directory as your Flask app
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Replace 'arcc_api_key' with the actual key retrieval mechanism
    arcc_api_key = "gt51b6ea"

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    status_code, response_data = post_files(file_path, arcc_api_key)
    os.remove(file_path)  # Clean up the saved file

    if status_code == 200:
        return jsonify(response_data), 200
    else:
        return jsonify({'error': 'Failed to upload file to Archetype AI'}), status_code


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

@app.route('/test', methods = ['POST'])
def hello_world():
    return 'Hello World'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('header.jsx')


@app.route('/upload_and_summarize', methods=['POST'])
def upload_and_summarize():
    arcc_api_key = "gt51b6ea"  # Use a secure way to store and retrieve this

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    # Process each file
    summaries = []
    file_ids = []
    for file in request.files.getlist('file'):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Assuming post_files function handles file upload correctly and returns a file ID or similar identifier
        status_code, response_data = post_files(file_path, arcc_api_key)
        os.remove(file_path)  # Clean up the saved file

        if status_code == 200:
            # Extract file identifier here, adjust as necessary
            file_id = response_data.get('file_id')
            file_ids.append(file_id)
            # Now call summarize with correct parameters, e.g., file ID
            status_code, summarize_data = script.summarize(file_ids, arcc_api_key)

            if status_code == 200:
                summary = script.get_summarized_test(summarize_data)
                summaries.append(summary)
            else:
                return jsonify({'error': 'Failed to summarize'}), status_code
        else:
            return jsonify({'error': 'Failed to upload file to Archetype AI'}), status_code

    # Assuming you want to return all summaries in a list
    return jsonify({"summaries": summaries}), 200

    
@app.route('/upload_and_analyze', methods=['POST'])
def upload_and_analyze():
    arcc_api_key = "gt51b6ea"
    file_ids = [] 
    text = request.form.get('prompt')
    address = request.form.get('address')
    for file in request.files.getlist('file'):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Assuming post_files function handles file upload correctly and returns a file ID or similar identifier
        status_code, response_data = post_files(file_path, arcc_api_key)
        os.remove(file_path)  # Clean up the saved file

        if status_code == 200:
            # Extract file identifier here, adjust as necessary
            file_id = response_data.get('file_id')
            file_ids.append(file_id)

        else:
            return jsonify({'error': 'Failed to upload file to Archetype AI'}), status_code

    # Process files and get combined summary
    Data_Summary = summarize_files_and_get_insights(file_ids, str(text))

    # Analyze sentiment and get combined score
    combined_score = analyze_sentiment_and_get_score(Data_Summary, str(address))

    return jsonify({'description': Data_Summary, 'combined_score': combined_score})



if __name__ == '__main__':
    app.run(port = 8000, debug=True)

