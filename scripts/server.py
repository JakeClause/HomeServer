from flask import Flask, render_template, send_from_directory, request, jsonify
from werkzeug.utils import secure_filename
import os
import shutil
import logging

app = Flask(__name__)


print("\nHit [Ctrl + C] to stop the server" + 
      "\nCheck the logs.txt file for debugging logs" + 
      "\nor visit https://192.168.6.194:5000/logs to view the logs in the browser." +
      "\n\n * or visit https://192.168.6.209:5000/logs if you are testing")

# Specify the upload folder on the server
UPLOAD_FOLDER = r'G:\HOMEFILETRASFER'

# Define subdirectories for different file types
SUBDIRECTORIES = {
    'movies': 'Movies',
    'tv_shows': 'TV Shows',
    'pdfs': 'PDFs',
    'other': 'Other'
}

# Create a dictionary to store directory paths
DIRECTORY_PATHS = {key: os.path.join(UPLOAD_FOLDER, value) for key, value in SUBDIRECTORIES.items()}

# Ensure the subdirectories exist
for directory_path in DIRECTORY_PATHS.values():
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# Function to get the download directory based on category
def get_download_directory(category):
    return DIRECTORY_PATHS.get(category, DIRECTORY_PATHS['other'])

# Function to determine the subdirectory based on file type
def get_subdirectory(file_name):
    file_extension = file_name.split('.')[-1].lower()
    if file_extension in ['mp4', 'avi', 'mkv', 'mov', 'flv', 'wmv']:
        return 'movies'
    elif file_extension == 'pdf':
        return 'pdfs'
    else:
        return 'other'

# Configure logging to write to a file
log_file = 'logs.txt'  # Change to your desired file path
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Debugging logs
logging.debug('Debugging logs enabled.')

# Endpoint for handling file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    logging.debug('Received file upload request.')
    
    if 'file' not in request.files:
        logging.error('No file part in request.')
        return 'No file part'

    files = request.files.getlist('file')  # Allow multiple files

    for file in files:
        if file.filename == '':
            logging.error('No selected file.')
            return 'No selected file'

        if file:
            # Ensure the directory exists
            destination = get_destination_directory(file)
            if not os.path.exists(destination):
                os.makedirs(destination)

            # Save the file or folder to the specified subdirectory
            if os.path.isdir(os.path.join(UPLOAD_FOLDER, file.filename)):
                # Handle folder upload
                copy_folder(os.path.join(UPLOAD_FOLDER, file.filename), destination)
            else:
                # Handle file upload
                filename = secure_filename(file.filename)
                file.save(os.path.join(destination, filename))
                logging.info('Uploading file: %s', filename)
    
    logging.info('File(s) uploaded successfully!')
    return 'File(s) uploaded successfully!'

# Function to get the destination directory
def get_destination_directory(file):
    # If the "Tv Shows" option is selected, place the folder inside the "TV Shows" folder
    category = request.form.get('category', 'other')
    if category == 'movies':
        destination = os.path.join(UPLOAD_FOLDER, 'Movies')
    elif category == 'tv_shows':
        destination = os.path.join(UPLOAD_FOLDER, 'TV Shows')
    elif category == 'pdfs':
        destination = os.path.join(UPLOAD_FOLDER, 'PDFs')
    else:
        destination = os.path.join(UPLOAD_FOLDER, 'Other')

    # If the file is uploaded inside a folder, create a corresponding folder structure
    if file.filename.count('/') > 0:
        folder_structure = os.path.join(destination, os.path.dirname(file.filename))
        destination = os.path.join(destination, folder_structure)
    return destination

# Function to recursively copy folder contents
def copy_folder(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy_folder(s, d)
        else:
            shutil.copy2(s, d)

# Endpoint for downloading files
@app.route('/download/<category>/<filename>')
def download_file(category, filename):
    download_directory = get_download_directory(category)
    return send_from_directory(download_directory, filename)

# Endpoint to get live logs
@app.route('/get_logs')
def get_logs():
    log_file_path = os.path.join(os.getcwd(), 'logs.txt')
    try:
        with open(log_file_path, 'r') as file:
            log_contents = file.readlines()[-100:]  # Read the last 100 lines
    except FileNotFoundError:
        log_contents = ['Log file not found.']
    return jsonify(log_contents)

# Endpoint to display logs
@app.route('/logs')
def display_logs():
    return render_template('logs.html', log_contents=[])

# Function to read log files
def read_logs():
    log_file_path = os.path.join(os.getcwd(), 'logs.txt')
    log_contents = []
    try:
        with open(log_file_path, 'r') as file:
            log_contents = file.readlines()[-100:]  # Read the last 100 lines
    except FileNotFoundError:
        log_contents = ['Log file not found.']
    return log_contents

@app.route('/')
def index():
    base_path = os.getcwd()  # Get the current working directory
    file_list = os.listdir(base_path)
    return render_template('hub.html', file_list=file_list)

# Endpoint for the "/hub" path
@app.route('/hub')
def hub():
    return render_template('hub.html')

# Endpoint for the "/dispo" path
@app.route('/dispo')
def dispo():
    return render_template('dispo.html')

# Endpoint for the "/upload" path
@app.route('/upload')
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(ssl_context=('./nginx/conf/cert.pem', './nginx/conf/key.pem'), host='0.0.0.0', port=5000)
