import os
import subprocess
import base64
import hashlib
import requests
from urllib.parse import urlparse

# Global variables
download_directory = 'downloads/'

# Key for encryption (keep it secret and safe)
key = b'my_secret_encryption_key'  # Replace with your own key, and keep it secure!

def encrypt_url(url):
    """Encrypt URL using base64 encoding."""
    encrypted_url = base64.urlsafe_b64encode(hashlib.sha256(url.encode()).digest()).rstrip(b'=')
    return encrypted_url

def decrypt_url(encrypted_url):
    """Decrypt URL using base64 decoding."""
    decrypted_url = base64.urlsafe_b64decode(encrypted_url + b'===')
    return decrypted_url.decode()

def get_random_headers():
    """Return random headers for the request."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    return headers

def download_file(encrypted_url):
    """Download file from the given URL."""
    url = decrypt_url(encrypted_url)
    headers = get_random_headers()
    
    try:
        with requests.Session() as session:
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                filename = get_filename_from_url(url, content_type)
                filepath = os.path.join(download_directory, filename)
                
                if 'mpegurl' in content_type or 'x-mpegURL' in content_type:  # Handle .m3u8 files
                    # Directly use ffmpeg to merge the m3u8 playlist into an mp4 file
                    video_filepath = os.path.join(download_directory, filename.replace('.m3u8', '.mp4'))
                    ffmpeg_path = './ffmpeg/bin/ffmpeg.exe'  # Adjust path as necessary
                    concat_command = [ffmpeg_path, '-i', url, '-c', 'copy', video_filepath]
                    subprocess.run(concat_command, check=True)
                    
                    print(f"Download completed: {video_filepath}")
                
                else:
                    with open(filepath, 'wb') as file:
                        file.write(response.content)
                    print(f"Download completed: {filepath}")
            
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred while downloading {url}: {str(e)}")

def get_filename_from_url(url, content_type):
    """Extract filename from URL and append correct extension based on content type."""
    parsed_url = urlparse(url)
    base_name = os.path.basename(parsed_url.path)
    if '.' not in base_name:
        return base_name + get_extension_from_content_type(content_type)
    return base_name

def get_extension_from_content_type(content_type):
    """Return file extension based on content type."""
    extensions = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'application/zip': '.zip',
        'application/pdf': '.pdf',
        'application/vnd.apple.mpegurl': '.m3u8',
        'video/mp4': '.mp4',
    }
    return extensions.get(content_type, '')

# Make sure the download directory exists
if not os.path.exists(download_directory):
    os.makedirs(download_directory)
