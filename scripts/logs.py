import os
import logging
from flask import Blueprint, render_template, jsonify

logs_bp = Blueprint('logs', __name__)

# Determine the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the log file relative to the directory of this script
log_file = os.path.join(script_dir, '..', 'logs.txt')  # Assuming logs.txt is in the parent directory

# Configure logging to write to the specified file
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to read log files
def read_logs():
    log_contents = []
    try:
        with open(log_file, 'r') as file:
            log_contents = file.readlines()[-100:]  # Read the last 100 lines
    except FileNotFoundError:
        log_contents = ['Log file not found.']
    return log_contents

# Function to clear log files
def clear_logs():
    try:
        open(log_file, 'w').close()  # Open the file in write mode, truncating the file to 0 length
        return True
    except Exception as e:
        return str(e)

@logs_bp.route('/get_logs')
def get_logs():
    try:
        log_contents = read_logs()
        return jsonify(log_contents)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@logs_bp.route('/display_logs')
def display_logs():
    log_contents = read_logs()
    return render_template('logs.html', logs=log_contents)

@logs_bp.route('/clear_logs')
def clear_logs_route():
    result = clear_logs()
    return jsonify({'success': result})
