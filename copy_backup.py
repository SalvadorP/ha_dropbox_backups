import os
import dropbox
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
LOCAL_FOLDER = os.getenv("LOCAL_FOLDER")
DROPBOX_FOLDER = os.getenv("DROPBOX_FOLDER")
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

def get_latest_modified_file(folder_path):
    files = []

    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        if os.path.isfile(full_path):
            files.append(full_path)
    if not files:
        return None

    # File with the last modified date.
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def upload_file_to_dropbox():
    if not LOCAL_FOLDER or not DROPBOX_FOLDER or not DROPBOX_ACCESS_TOKEN:
        print("Error: Missing configuration in .env file.")
        return

    latest_file = get_latest_modified_file(LOCAL_FOLDER)
    if not latest_file:
        print("No files found in the specified folder.")
        return

    file_name = os.path.basename(latest_file)

    with open(latest_file, "rb") as f:
        try:
            dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
            dropbox_path = os.path.join(DROPBOX_FOLDER, file_name)

            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
            print(f"Uploaded {file_name} to Dropbox folder {DROPBOX_FOLDER}")
        except Exception as e:
            print(f"Error uploading file: {e}")

if __name__ == "__main__":
    upload_file_to_dropbox()
