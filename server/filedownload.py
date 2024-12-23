import os
import pysftp
from datetime import datetime, timedelta

def sftp_download_file(host, username, password, remote_folder_name, local_folder_name, port=22):
    """
    Connect to an SFTP server, locate a specific file based on date, and download it.

    :param host: SFTP server host address
    :param username: SFTP username
    :param password: SFTP password
    :param remote_folder_name: Path to the folder on the SFTP server
    :param local_folder_name: Local folder name where the file should be downloaded
    :param port: Port for SFTP connection (default is 22)
    """
    try:
        # Define the connection options
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # Use this for servers without known host keys

        print("Connecting to SFTP server...")
        with pysftp.Connection(host, username=username, password=password, port=port, cnopts=cnopts) as sftp:
            print("Connected to SFTP server.")

            # List files in the remote directory
            print("Listing files in the remote directory...")
            files = sftp.listdir(remote_folder_name)
            print("Files available:", files)

            # Generate the file name based on the previous date
            

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace these values with your actual SFTP details
    host = "sftp.example.com"
    username = "your_username"
    password = "your_password"
    remote_folder_name = "/from_ICE"
    local_folder_name = "downloads"  # Local folder relative to script directory

    # Call the function to download a file based on the previous date
    sftp_download_file(host, username, password, remote_folder_name, local_folder_name)
