from flask import Blueprint, send_from_directory
import os
import json

download_bp = Blueprint('download', __name__)

with open('settings.json') as f:
    settings = json.load(f)

# Specify the upload folder on the server
UPLOAD_FOLDER = settings.get('HOMEFILETRANSFER')

# Define subdirectories for different file types
SUBDIRECTORIES = {
    'movies': 'Movies',
    'tv_shows': 'TV Shows',
    'pdfs': 'PDFs',
    'other': 'Other'
}

# Function to get the download directory based on category
def get_download_directory(category):
    return os.path.join(UPLOAD_FOLDER, SUBDIRECTORIES.get(category, 'Other'))

@download_bp.route('/download/<category>/<filename>')
def download_file(category, filename):
    download_directory = get_download_directory(category)
    return send_from_directory(download_directory, filename)
