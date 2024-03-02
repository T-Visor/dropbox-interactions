#!/usr/bin/env python3

import dropbox
import os
import sys
import re
import dotenv


def main():
    """
        Precondition:
            Access token created on Dropbox account with permission for 'files.content.write' enabled.

        Description: 
            Upload a local file to Dropbox.

        Usage: 
            python3 dropbox-upload.py <local_file_path> <dropbox_file_path>
    """
    # Load environment variables from the '.env' file
    dotenv.load_dotenv()

    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print('Usage: python dropbox-upload.py <local_file_path>')
        return

    # Parse command-line arguments
    local_file_path = sys.argv[1]
    dropbox_file_path = sys.argv[2]

    # Check if the local file exists
    if not does_local_file_exist(local_file_path):
        print(f'Local file "{local_file_path}" does not exist.')
        return

    # Check if supplied Dropbox file path is valid
    if not is_valid_unix_file_path(dropbox_file_path):
        print(f'Dropbox file_path "{dropbox_file_path}" is not a valid pathname')
        return

    # Load the access token for Dropbox
    dropbox_access_token = os.getenv('DROPBOX_ACCESS_TOKEN')
    if not dropbox_access_token:
        print(f'Dropbox access token could not be loaded from ".env" file')
        return

    # Proceed to upload to Dropbox
    print(f'SOURCE: {local_file_path}')
    print(f'DESTINATION: {dropbox_file_path}\n')
    upload_to_dropbox(local_file_path, dropbox_file_path, dropbox_access_token)


def does_local_file_exist(file_path: str) -> bool:
    """
        Arguments:
            file_path (str): local file path

        Returns: 
            'True' if the file exists
            'False' otherwise
    """
    return is_valid_unix_file_path(file_path) and os.path.exists(file_path)


def is_valid_unix_file_path(file_path: str) -> bool:
    """
        Arguments:
            file_path (str): file path (local or remote machine)

        Returns: 
            'True' if the file path is a valid Unix file path
            'False' otherwise
    """
    # Checks to see if the supplied string has the following characteristics:
    # 
    # Starts with a forward slash '/'
    # One or more occurrences of a word
    # Optionally contains an ending forward slash '/'
    pattern = r'^\/(?:[\w.-]+\/?)+$'
    return re.match(pattern, file_path) is not None


def upload_to_dropbox(local_file_path: str, dropbox_file_path: str, access_token: str):
    """
        Description:
            Upload the file to the location on Dropbox.

        Arguments:
            local_file_path (str): the source file to upload

            dropbox_file_path (str): the destination file path 

            access_token (str): access token to connect to Dropbox account
    """
    # Authenticate with Dropbox
    dropbox_connection = dropbox.Dropbox(access_token)

    # Upload the file
    with open(local_file_path, 'rb') as f:
        try:
            dropbox_connection.files_upload(f.read(), dropbox_file_path)
            print(f'SUCCESS: File "{local_file_path}" uploaded to Dropbox as "{dropbox_file_path}"')
        except dropbox.exceptions.ApiError as e:
            print(f'Error uploading file to Dropbox: {e}')


if __name__ == '__main__':
    main()
