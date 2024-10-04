import paramiko
import os

# Function to download a file from the SFTP server
def download_file_from_sftp(host, port, username, password, remote_file_path, local_file_path):
    try:
        # Create an SFTP client object
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Uncomment this section to search for the file dynamically
        # Directory to search for the file on the SFTP server
        # remote_directory = '/path/to/remote/directory'
        # for file in sftp.listdir(remote_directory):
        #     if 'ice_volume' in file:
        #         remote_file_path = os.path.join(remote_directory, file)
        #         print(f"Found file: {remote_file_path}")
        #         break

        # Download the file to a local path
        sftp.get(remote_file_path, local_file_path)
        print(f"File downloaded successfully to {local_file_path}")

        # Close the SFTP connection
        sftp.close()
        transport.close()

    except Exception as e:
        print(f"Error: {e}")

# Mock credentials (replace with actual values when available)
sftp_host = "sftp.icewebsite.com"  # Mock host
sftp_port = 22  # Default SFTP port
sftp_username = "your_username"
sftp_password = "your_password"

# Mock file paths
remote_file = "/path/to/remote/ice_volume"  # Replace with actual file path on SFTP server
local_file = "y/Ice/ice_volume"  # Destination path on local machine

# Call the function to download the file
download_file_from_sftp(sftp_host, sftp_port, sftp_username, sftp_password, remote_file, local_file)
