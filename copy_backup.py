import os
from dotenv import load_dotenv
import dropbox  # Ensure this is imported for accessing the `dropbox.files` namespace
from dropbox.exceptions import AuthError
from datetime import datetime

load_dotenv()
LOCAL_FOLDER = os.getenv("LOCAL_FOLDER")
DROPBOX_FOLDER = os.getenv("DROPBOX_FOLDER")
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SECRET = os.getenv("DROPBOX_APP_SECRET")

def get_dropbox_client():
    try:
        print(f"APP_KEY: {APP_KEY}, APP_SECRET: {APP_SECRET}, REFRESH_TOKEN: {DROPBOX_TOKEN}")

        dbx = dropbox.Dropbox(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            oauth2_refresh_token=DROPBOX_TOKEN,
        )
        return dbx
    except AuthError as e:
        print(f"Failed to authenticate with Dropbox: {e}")
        return None

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
    if not LOCAL_FOLDER or not DROPBOX_FOLDER or not DROPBOX_TOKEN:
        print("Error: Missing configuration in .env file.")
        return

    dbx = get_dropbox_client()
    if not dbx:
        return

    latest_file = get_latest_modified_file(LOCAL_FOLDER)
    if not latest_file:
        print("No files found in the specified folder.")
        return

    file_name = os.path.basename(latest_file)

    with open(latest_file, "rb") as f:
        try:
            dropbox_path = os.path.join(DROPBOX_FOLDER, file_name)
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
            print(f"Uploaded {file_name} to Dropbox folder {DROPBOX_FOLDER}")
        except Exception as e:
            print(f"Error uploading file: {e}")

if __name__ == "__main__":
    upload_file_to_dropbox()
