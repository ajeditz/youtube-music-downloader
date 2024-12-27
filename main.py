import os
import subprocess

def download_youtube_music_yt_dlp(playlist_url, save_path='downloads/'):
    """
    Downloads all songs from a YouTube Music playlist as MP3 using yt-dlp.
    
    :param playlist_url: URL of the YouTube Music playlist
    :param save_path: Directory to save downloaded MP3 files
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    try:
        # Use yt-dlp to download and convert audio to MP3
        command = [
            "yt-dlp",
            "--extract-audio",  # Extract only audio
            "--audio-format", "mp3",  # Convert to MP3
            "--audio-quality", "0",  # Best quality
            "-o", f"{save_path}/%(title)s.%(ext)s",  # Save format
            playlist_url
        ]
        subprocess.run(command)
        print("All songs downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace with your YouTube Music playlist URL
    liked_playlist_url = "https://music.youtube.com/playlist?list=PLZrpP5dYrtclRqk7lmb4FPiy0HrCNUiiK&feature=shared"
    download_youtube_music_yt_dlp(liked_playlist_url)
