import yt_dlp
from moviepy.editor import VideoFileClip
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError
import os
import logging

def download_video(url, output_path):
    logging.info(f"Downloading video from {url}")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    ffmpeg_location = r'C:\Users\jakec\Desktop\uploadServer (Upto Date)\ffmpeg\bin\ffmpeg.exe'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Use the video's default title
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_location
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        default_filename = os.path.join(output_path, f"{info['title']}.mp3")  # Get the default filename
    return default_filename


def rename_file(file_path, new_name):
    # Ensure the new name ends with .mp3
    if not new_name.endswith('.mp3'):
        new_name += '.mp3'

    # Construct the new file path
    new_file_path = os.path.join(os.path.dirname(file_path), new_name)
    
    # Rename the file
    os.rename(file_path, new_file_path)
    logging.info(f"File renamed to {new_name}")
    return new_file_path


def convert_to_mp3(video_path):
    logging.info(f"Converting video to mp3: {video_path}")
    mp3_path = os.path.splitext(video_path)[0] + '.mp3'
    video = VideoFileClip(video_path)
    try:
        video.audio.write_audiofile(mp3_path)
    except Exception as e:
        print(f"Error during audio conversion: {e}")
    finally:
        video.close()
    return mp3_path


def cleanup_file(file_path):
    logging.info(f"Cleaning up file: {file_path}")
    if os.path.exists(file_path):
        os.remove(file_path)

# This is not working correctly 
def update_metadata(mp3_path, artist, title):
    try:
        new_album = "."
        audio = EasyID3(mp3_path)
        audio["artist"] = artist
        audio["title"] = title
        audio['album'] = new_album
        audio.save()
        print(f"Updated: {mp3_path}")
    except ID3NoHeaderError:
        audio = ID3(mp3_path)
        audio.add(ID3.TALB(encoding=3, text=artist))
        audio.add(ID3.TALB(encoding=3, text=new_album))
        audio.add(ID3.TIT2(encoding=3, text=title))
        audio.save()
        print(f"Created ID3 and updated: {os.path.basename(mp3_path)}")
    except Exception as e:
        print(f"Error updating {os.path.basename(mp3_path)}: {e}")
    return mp3_path
