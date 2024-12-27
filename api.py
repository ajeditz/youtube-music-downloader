from fastapi import FastAPI
from main import download_youtube_music_yt_dlp
from fastapi.middleware.cors import CORSMiddleware
from pprint import pprint


app=FastAPI(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



app=FastAPI()


#WORK IN PROGRESS


@app.route('/download')
def download(playlist_url:str):
    download_youtube_music_yt_dlp(playlist_url)
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import os
import subprocess
import shutil
from pathlib import Path
import uuid

app = FastAPI()

DOWNLOAD_DIR = "downloads"

@app.post("/download_playlist/")
async def download_playlist(playlist_url: str = Form(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Endpoint to download a YouTube playlist as MP3 files and return a ZIP for download.
    :param playlist_url: The YouTube playlist URL
    :param background_tasks: Tasks to clean up files after serving
    """
    # Unique folder for the session
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(DOWNLOAD_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)

    try:
        # Download playlist as MP3 using yt-dlp
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", f"{session_dir}/%(title)s.%(ext)s",
            playlist_url,
        ]
        subprocess.run(command, check=True)

        # Create a ZIP file
        zip_file = f"{session_dir}.zip"
        shutil.make_archive(session_dir, 'zip', session_dir)

        # Schedule cleanup
        background_tasks.add_task(shutil.rmtree, session_dir)  # Delete folder
        background_tasks.add_task(os.remove, zip_file)  # Delete zip after serving

        return FileResponse(zip_file, media_type='application/zip', filename="playlist.zip")
    except Exception as e:
        shutil.rmtree(session_dir, ignore_errors=True)  # Clean up on error
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
async def root():
    return {"message": "API is running!"}
