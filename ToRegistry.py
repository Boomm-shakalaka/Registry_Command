import os
import requests
import argparse

def upload_to_registry(args):
    # Base URL for the add_data endpoint
    url = "http://127.0.0.1:5000/add_data"

    # Prepare data for POST request
    data = {
        'dataset_name': args.dataset_name,
        'summary_data_link': args.summary_data_link
    }

    # Prepare files for POST request
    for file in os.listdir(args.raw_data_folder):
        raw_data_files = [('raw_data_folder', open(os.path.join(args.raw_data_folder, file), 'rb'))]
    for file in os.listdir(args.processed_data_folder):
        processed_data_files = [('processed_data_folder', open(os.path.join(args.processed_data_folder, file), 'rb')) ]

    # Combine data and files for the POST request
    payload = {'dataset_name': args.dataset_name, 'summary_data_link': args.summary_data_link}
    files = raw_data_files + processed_data_files

    # Send POST request
    response = requests.post(url, data=payload, files=files)

    # Check the response status
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

    upload_to_registry(args)


