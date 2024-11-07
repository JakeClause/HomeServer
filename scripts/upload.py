from flask import Blueprint, request, jsonify, send_from_directory
import os
import shutil
from werkzeug.utils import secure_filename
import logging
import json

upload_bp = Blueprint('upload', __name__)

with open('settings.json') as f:
    settings = json.load(f)

# Specify the upload folder on the server
#UPLOAD_FOLDER = r'C:\Users\jakec\Desktop\test'
UPLOAD_FOLDER = settings.get('HOMEFILETRASFER')

# Define subdirectories for different file types
SUBDIRECTORIES = {
    'movies': 'Movies',
    'tv_shows': 'TV Shows',
    'pdfs': 'PDFs',
    'music': 'Music',
    'other': 'Other'
}

# Function to get the download directory based on category
def get_download_directory(category):
    return os.path.join(UPLOAD_FOLDER, SUBDIRECTORIES.get(category, 'Other'))

# Function to determine the subdirectory based on file type
def get_subdirectory(file_name):
    file_extension = file_name.split('.')[-1].lower()
    if file_extension in ['mp4', 'avi', 'mkv', 'mov', 'flv', 'wmv']:
        return 'movies'
    if file_extension in ['wav', 'flac', 'mp3']:
        return 'music'
    elif file_extension == 'pdf':
        return 'pdfs'
    else:
        return 'other'

@upload_bp.route('/upload', methods=['POST'])
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
            # Determine the subdirectory based on the file type
            subdirectory = get_subdirectory(file.filename)
            destination = os.path.join(UPLOAD_FOLDER, SUBDIRECTORIES.get(subdirectory, 'Other'))

            # Ensure the directory exists
            if not os.path.exists(destination):
                os.makedirs(destination)

            # Save the file to the specified subdirectory
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
    elif category == 'music':
        destination = os.path.join(UPLOAD_FOLDER, 'Music')
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
@upload_bp.route('/download/<category>/<filename>')  # Fixed this line
def download_file(category, filename):
    download_directory = get_download_directory(category)
    return send_from_directory(download_directory, filename)
