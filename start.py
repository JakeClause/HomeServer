
# Features:
#------------
# - Login page
# - Hub page
# User:
# - Animation Hub
# - Dispo page
# - Link to weather
# - Link to Plex Dashboard
# - Server Logs Viewer
# - Request a movie
# Admin:
# - File browser to view files in the file transfer folder
# - PDF to JPG conversion
# - File upload
# - YouTube to MP3 conversion
# - Settings page to change the file transfer folder
# - Server logs
# - Movie requests Viewer
# - DizqueTV server status (NOT ACTIVATED BUT WORKS)
#
############################################################################################################## Imports
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from scripts.upload import upload_bp
from scripts.download import download_bp
from scripts.logs import logs_bp  # Import the logs_bp blueprint
from scripts.pdf import pdf_to_jpg  # Import the pdf_to_jpg function
from scripts.youtube_to_mp3 import download_video, update_metadata, convert_to_mp3, cleanup_file, rename_file
import scripts.url_downloader as url_downloader
import logging
import psutil
import os
import subprocess
import requests
import json
import platform

############################################################################################################## Flask App Configuration
# Load settings from JSON file
with open('settings.json') as f:
    settings = json.load(f)

# Directory path where videos are stored
VIDEO_DIRECTORY = r'G:\To Transfer\other\Misc'  # Use raw string for Windows path
# Main directory path
MAIN_FOLDER = settings.get("HOMEFILETRASFER") # Change this path to the location of the folder where the uploaded files will be saved (logging purposes)    
# Directory path where the converted JPG files will be saved
PDF_DOWNLOAD_FOLDER = MAIN_FOLDER +'/PDFs' # Change this path to the location of the folder where the converted JPG files will be saved (logging purposes)
MP3_DOWNLOAD_FOLDER = MAIN_FOLDER +'/Music' # Change this path to the location of the folder where the converted MP3 files will be saved (logging purposes)
# Path to the DizqueTV executable file
#DIZQUETV_EXE_PATH = "C:/Users/jakec/Desktop/New PC/plex/dizquetv-win-x64.exe" # Change this path to the location of the dizquetv-win-x64.exe file (logging purposes)

#PDF_DOWNLOAD_FOLDER = "C:/Users/jakec/OneDrive/Desktop/home-server/pdfs" 
#DIZQUETV_EXE_PATH = "C:/Users/jakec/Desktop/OneDrive/home-server/.dizquetv/dizquetv-win-x64.exe" # Change this path to the location of the dizquetv-win-x64.exe file (logging purposes)



app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random secret key

# Register blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(download_bp, url_prefix='/download')
app.register_blueprint(logs_bp, url_prefix='/logs')  # Register the logs_bp blueprint
app.config['UPLOAD_FOLDER'] = PDF_DOWNLOAD_FOLDER 

############################################################################################################## Logging
log_file = 'logs.txt'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Change ip (logging purposes)
print("\nHit [Ctrl + C] to stop the server" + 
"\nCheck the logs.txt file for debugging logs" + 
"\n * or visit REMOVED_IP to view the logs in the browser." +
"\n * or visit REMOVED_IP for the hub." + 
"\n * or visit REMOVED_IP for debugging")



############################################################################################################## Movie Request
# File path for storing movie requests
requests_file = 'movie_requests.txt'

# Initialize movie requests from the file
def load_requests():
    try:
        with open(requests_file, 'r') as file:
            requests = file.read().splitlines()
        return requests
    except FileNotFoundError:
        return []

movie_requests = load_requests()

# Render the movie request page
@app.route('/requests')
def request_movie():
    return render_template('request_movie.html')

# Save movie requests to the file
def save_requests():
    with open(requests_file, 'w') as file:
        file.write('\n'.join(movie_requests))

# Endpoint to add a movie request
@app.route('/requests/add_request', methods=['POST'])
def add_request():
    movie_title = request.form.get('movie_title')
    if movie_title:
        movie_requests.append(movie_title)
        save_requests()
        return jsonify(success=True)
    else:
        return jsonify(success=False, error='Movie title not provided')

# Endpoint to get all movie requests
@app.route('/requests/get_requests', methods=['GET'])
def get_requests():
    return jsonify(movie_requests)

# Endpoint to clear all movie requests
@app.route('/requests/clear_requests', methods=['GET'])
def clear_requests():
    movie_requests.clear()
    save_requests()
    return jsonify(success=True)


############################################################################################################## Main Page
@app.route('/')
def main_page():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('hub'))
    else:
        return render_template('login.html')

############################################################################################################## Login

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'ASjoi12lim!':
        session['logged_in'] = True
        return redirect(url_for('hub'))
    else:
        return render_template('login.html', error="Invalid password")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('hub'))

############################################################################################################## Hub

@app.route('/hub')
def index():
    base_path = os.getcwd()  # Get the current working directory
    file_list = os.listdir(base_path)
    return render_template('hub.html', file_list=file_list)

@app.route('/hub')
def hub():
    return render_template('hub.html')

@app.route('/dispo')
def dispo():
    return render_template('dispo.html')

############################################################################################################## Animation Hub

@app.route('/animations', methods=['GET'])
def animations():
    return render_template('animationhub.html')

@app.route('/a_bounce', methods=['GET'])
def a_bounce():
    return render_template('a_bounce.html')

@app.route('/a_circle', methods=['GET'])
def a_circle():
    return render_template('a_circle.html')

@app.route('/a_triangle', methods=['GET'])
def a_triangle():
    return render_template('a_triangle.html')

@app.route('/a_water', methods=['GET'])
def a_water():
    return render_template('a_water.html')

############################################################################################################## Settings
# Load settings from JSON file
def load_settings():
    with open('settings.json') as f:
        return json.load(f)

# Save settings to JSON file
def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

@app.route('/settings', methods=['GET'])
def settings():
    with open('settings.json', 'r') as f:
        settings_data = json.load(f)
    return render_template('settings.html', folder=settings_data)

# Route for saving settings
@app.route('/save_settings', methods=['POST'])
def save_settings_handler():
    settings_data = load_settings()
    settings_data['HOMEFILETRASFER'] = request.form.get('HOMEFILETRASFER')
    settings_data['PDF'] = request.form.get('PDF')
    save_settings(settings_data)
    return redirect(url_for('settings'))

############################################################################################################## About pc

def get_system_info():
    system_info = {
        'System': platform.system(),
        'Node Name': platform.node(),
        'Machine': platform.machine(),
        'Processor': platform.processor()
    }
    return system_info

@app.route('/about_pc', methods=['GET'])
def about_pc():
    system_info = get_system_info()
    return render_template('pc_about.html', system_info=system_info)


############################################################################################################## File Browser

# File Browser Route
@app.route('/file_browser')
def file_browser():
    path = request.args.get('path', MAIN_FOLDER)
    if not os.path.exists(path):
        return "Path does not exist", 404

    file_data = []
    try:
        for entry in os.scandir(path):
            file_data.append({
                'path': entry.path,
                'is_dir': entry.is_dir()
            })
    except PermissionError:
        return "Permission denied", 403

    if 'logged_in' in session and session['logged_in']:
        return render_template('file_browser.html', current_path=path, file_data=file_data, root_path=MAIN_FOLDER)
    else:
        return render_template('login.html')
    



############################################################################################################## PDF Conversion

@app.route('/pdf', methods=['GET'])
def render_pdf():
    if 'logged_in' in session and session['logged_in']:
        return render_template('pdftojpg.html', download_folder=PDF_DOWNLOAD_FOLDER)
    else:
        return render_template('login.html')

@app.route('/pdf', methods=['POST'])
def convert():
    logging.info('PDF conversion request received.')
    input_file = request.files['pdfFile']  # Get the uploaded PDF file
    output_folder = PDF_DOWNLOAD_FOLDER  # Use the fixed destination folder

    if input_file.filename == '':
        return 'No selected file'

    if input_file.filename.endswith(".pdf"):
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file.filename)
        os.makedirs(output_folder, exist_ok=True)
        logging.info(f'Converting {pdf_path} to JPG in {output_folder}')
        input_file.save(pdf_path)
        pdf_to_jpg(pdf_path, output_folder)  # Use the pdf_to_jpg function
        logging.info('PDF conversion complete.')
        return 'Conversion complete.'
    else:
        return 'Invalid file format'

############################################################################################################## File Upload

@app.route('/upload_file', methods=['GET'])
def render_upload_form():
    if 'logged_in' in session and session['logged_in']:
        return render_template('upload.html')
    else:
        return render_template('login.html')
    

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part'
        
        # Get the list of uploaded files
        uploaded_files = request.files.getlist('file')

        # Process each uploaded file
        for uploaded_file in uploaded_files:
            # Check if the file has a filename
            if uploaded_file.filename == '':
                return 'No selected file'
   
    # If the request method is not POST, return an error response
    return 'Method Not Allowed', 405

############################################################################################################## YouTube2MP3

@app.route('/youtube2mp3', methods=['GET'])
def youtube2mp3():
    if 'logged_in' in session and session['logged_in']:
        return render_template('youtube2mp3.html')
    else:
        return render_template('login.html')

@app.route('/youtube2mp3', methods=['POST'])
def youtube2mp3_convert():
    url = request.form.get('url')
    name = request.form.get('name')
    output_path = MP3_DOWNLOAD_FOLDER
    try:
        # Download video with the default name
        video_path = download_video(url, output_path)
        # Rename the MP3 file to the desired name
        renamed_path = rename_file(video_path, name)
        # grabs the title and artist of the mp3 file (artist - title)
        artist, title = name.split(' - ')
        logging.info(f"Artist: {artist} Title: {title}")
        # update metadata
        update_metadata(renamed_path, artist, title)
        logging.info(f'YouTube download complete: {renamed_path}')
        return send_from_directory(directory=os.path.dirname(renamed_path), path=os.path.basename(renamed_path), as_attachment=True)
    except Exception as e:
        logging.error(f'Error occurred during YouTube download: {str(e)}')
        return f'Error occurred during YouTube download: {str(e)}'



############################################################################################################## Audio Download

@app.route('/download_audio', methods=['POST'])
def download_audio():
    url = request.form['url']
    download_path = os.path.join(MAIN_FOLDER, "downloaded_audio.mp3")
    try:
        result = subprocess.run(['you-get', '-o', MAIN_FOLDER, '--format=mp3', url], capture_output=True, text=True)
        if result.returncode == 0:
            return send_from_directory(directory=MAIN_FOLDER, path="downloaded_audio.mp3", as_attachment=True)
        else:
            return 'Error occurred during audio download', 500
    except Exception as e:
        return f'Error occurred: {str(e)}', 500


############################################################################################################## Video Viewer
def get_video_files(directory):
    videos = []
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            videos.append(filename)
    return videos

@app.route('/video_hub')
def video_hub():
    if 'logged_in' in session and session['logged_in']:
        return render_template('gridhub.html')
    else:
        return render_template('login.html')
    

@app.route('/get_videos')
def get_videos():
    videos = get_video_files(VIDEO_DIRECTORY)
    return jsonify(videos)

@app.route('/watch/<path:video_file>')
def watch(video_file):
    if os.path.isfile(os.path.join(VIDEO_DIRECTORY, video_file)):
        if 'logged_in' in session and session['logged_in']:
            return render_template('watch.html', video_file=video_file)
        elif not 'logged_in' in session or not session['logged_in']:
            return render_template('login.html')
        else:
            return '404 Not Found', 404

# Serve video files with correct MIME type
@app.route('/videos/<path:video_file>')
def serve_video(video_file):
    if video_file in get_video_files(VIDEO_DIRECTORY):
        return send_from_directory(VIDEO_DIRECTORY, video_file, mimetype='video/mp4')
    else:
        return '404 Not Found', 404

# Serve static files from the 'static' directory
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


############################################################################################################## url_downloader
@app.route('/download_url', methods=['GET'])
def show_url_form():
    if 'logged_in' in session and session['logged_in']:
        return render_template('url_download.html')
    else:
        return render_template('login.html')

@app.route('/download_url', methods=['POST'])
def download_url():
    if 'logged_in' in session and session['logged_in']:
        url = request.form.get('url')
        if url:
            encrypted_url = encrypt_url(url)
            download_file(encrypted_url)
            return jsonify(success=True, message="Download started")
        else:
            return jsonify(success=False, message="No URL provided")
    else:
        return render_template('login.html')

############################################################################################################## Storage

def get_drive_info(drive):
    try:
        # Get disk usage
        usage = psutil.disk_usage(drive)
        
        # Convert bytes to GB
        total_gb = usage.total / (1024 ** 3)
        used_gb = usage.used / (1024 ** 3)
        free_gb = usage.free / (1024 ** 3)

        # Convert GB to TB if needed
        if total_gb >= 1024:
            total_tb = total_gb / 1024
            used_tb = used_gb / 1024
            free_tb = free_gb / 1024
            return {
                'total': total_tb,
                'used': used_tb,
                'free': free_tb,
                'unit': 'TB'
            }
        else:
            return {
                'total': total_gb,
                'used': used_gb,
                'free': free_gb,
                'unit': 'GB'
            }
    except Exception as e:
        return {
            'total': 0,
            'used': 0,
            'free': 0,
            'unit': 'GB',
            'error': str(e)
        }

@app.route('/disk-info')
def disk_info():
    drives = [part.mountpoint for part in psutil.disk_partitions()]
    drive_info = {drive: get_drive_info(drive) for drive in drives}
    return jsonify(drive_info)


############################################################################################################## Run the Flask App
if __name__ == '__main__':
    app.run(ssl_context=('./nginx/conf/cert.pem', './nginx/conf/key.pem'), host='0.0.0.0', port=5000)


############################################################################################################## DizqueTV Server Status

# Function to scrape the DizqueTV server status from the webpage
#def get_dizquetv_status():
#    try:
#        response = requests.get(DIZQUETV_WEBPAGE_URL)
#        if response.status_code == 200:
#            return "Online"
#        else:
#            return "Offline"
#    except Exception as e:
#        logging.error("Error retrieving DizqueTV server status: %s", e)
#        return "Unknown"

# Route to launch the dizquetv-win-x64.exe process
#@app.route('/launch', methods=['POST'])
#def launch_dizquetv():
#    try:
#        subprocess.Popen([DIZQUETV_EXE_PATH], shell=True)
#        logging.info('dizquetv-win-x64.exe launched successfully.')
#        return jsonify({'status': 'success', 'message': 'Server launched successfully!'})
#    except Exception as e:
#        logging.error(f'Error launching dizquetv-win-x64.exe: {str(e)}')
#        return jsonify({'status': 'error', 'message': f'Error launching server: {str(e)}'})

# Route to close the dizquetv-win-x64.exe process
#@app.route('/close', methods=['POST'])
#def close_dizquetv():
#    try:
#        subprocess.Popen(["taskkill", "/f", "/im", "dizquetv-win-x64.exe"])
#        logging.info('dizquetv-win-x64.exe closed successfully.')
#        return jsonify({'status': 'success', 'message': 'Server closed successfully!'})
#    except Exception as e:
#        logging.error(f'Error closing dizquetv-win-x64.exe: {str(e)}')
#        return jsonify({'status': 'error', 'message': f'Error closing server: {str(e)}'})

# Route to render the dizquetv.html page
#@app.route('/dizquetv')
#def dizquetv():
    # Get the DizqueTV server status
#    status = get_dizquetv_status()
#    return render_template('dizquetv.html', server_status=status)