import os
import requests
import argparse
from werkzeug.utils import secure_filename

def uplaod_to_registry(args):
    url = "http://127.0.0.1:5000/add_data"

    # Prepare data for POST request
    data = {
        'dataset_name': args.dataset_name,
        'summary_data_link': args.summary_data_link
    }
    for uploaded_file in os.listdir(args.raw_data_folder):
        # Ensure a safe filename using secure_filename
        filename = secure_filename(uploaded_file)
        file_path = os.path.join(args.raw_data_folder, uploaded_file)

        # Include file in the 'files' parameter of the request
        files = {'file': (filename, open(file_path, 'rb'))}

        # Include other data in the 'data' parameter of the request
        response = requests.post(url, data=data, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"File {filename} uploaded successfully.")
        else:
            print(f"Failed to upload file {filename}. Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Data added successfully for dataset: {args.dataset_name}")
    else:
        print(f"Failed to add data. Status code: {response.status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add data via command line.")
    parser.add_argument('--dataset_name', '-dn', dest='dataset_name', required=True, help="Name of the dataset")
    parser.add_argument('--raw_data_folder', '-rdf', dest='raw_data_folder', required=True, help="Path to raw data folder")
    parser.add_argument('--processed_data_folder', '-pdf', dest='processed_data_folder', required=True, help="Path to processed data folder")
    parser.add_argument('--summary_data_link', '-sdl', dest='summary_data_link', required=True, help="Summary data link")
    args = parser.parse_args()

    uplaod_to_registry(args)