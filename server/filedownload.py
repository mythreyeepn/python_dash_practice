import os
import pysftp
from datetime import datetime, timedelta

def sftp_download_from_folder(host, username, password, remote_folder_path, local_download_path, port=22):
    """
    Connect to an SFTP server, locate a specific file based on date, and download it.

    :param host: SFTP server host address
    :param username: SFTP username
    :param password: SFTP password
    :param remote_folder_path: Path to the folder on the SFTP server
    :param local_download_path: Local path where the file should be downloaded
    :param port: Port for SFTP connection (default is 22)
    """
    try:
        # Define the connection options
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # Use this for servers without known host keys

        print("Connecting to SFTP server...")
        with pysftp.Connection(host, username=username, password=password, port=port, cnopts=cnopts) as sftp:
            print("Connected to SFTP server.")

            # Check if the remote folder exists
            if not sftp.exists(remote_folder_path):
                print(f"Error: The remote folder {remote_folder_path} does not exist.")
                return

            # Generate the file name based on the previous date
            previous_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d0600")
            file_to_download = f"ICC_ICEU_volume_V2_{previous_date}.csv"
            remote_file_path = os.path.join(remote_folder_path, file_to_download)

            # Check if the specific file exists
            if not sftp.exists(remote_file_path):
                print(f"Error: The file {file_to_download} does not exist in the folder {remote_folder_path}.")
                return

            # Ensure the local download path directory exists
            os.makedirs(os.path.dirname(local_download_path), exist_ok=True)

            print(f"Downloading file {file_to_download} from {remote_file_path} to {local_download_path}...")
            sftp.get(remote_file_path, local_download_path)
            print("File downloaded successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace these values with your actual SFTP details
    host = "sftp.example.com"
    username = "your_username"
    password = "your_password"
    remote_folder_path = "/from_ICE"
    local_download_path = "path/to/local/destination/file.txt"

    # Call the function to download a file based on the previous date
    sftp_download_from_folder(host, username, password, remote_folder_path, local_download_path)
