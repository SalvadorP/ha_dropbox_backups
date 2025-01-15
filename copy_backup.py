import os
from dotenv import load_dotenv
import dropbox
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# Retrieve configurations
LOCAL_FOLDER = os.getenv("LOCAL_FOLDER")
DROPBOX_FOLDER = os.getenv("DROPBOX_FOLDER")
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

def upload_file_to_dropbox():
    # Validate configurations
    if not LOCAL_FOLDER or not DROPBOX_FOLDER or not DROPBOX_ACCESS_TOKEN:
        print("Error: Missing configuration in .env file.")
        return

    # Get the current date for file selection
    today = datetime.now().strftime("%Y-%m-%d")

    # Find the file to upload
    for file_name in os.listdir(LOCAL_FOLDER):
        if today in file_name:  # Customize this condition if necessary
            local_file_path = os.path.join(LOCAL_FOLDER, file_name)

            if os.path.isfile(local_file_path):
                # Upload the file
                with open(local_file_path, "rb") as f:
                    try:
                        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
                        dropbox_path = os.path.join(DROPBOX_FOLDER, file_name)

                        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
                        print(f"Uploaded {file_name} to Dropbox folder {DROPBOX_FOLDER}")
                        return
                    except Exception as e:
                        print(f"Error uploading file: {e}")
                        return

    print("No file found to upload.")

if __name__ == "__main__":
    upload_file_to_dropbox()
