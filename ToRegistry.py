import os
import re
import requests
import argparse
from bs4 import BeautifulSoup

def upload_to_registry(args):
    # Base URL for the add_data endpoint
    url_root = "http://127.0.0.1:5000"
    url_add_data="http://127.0.0.1:5000/add_data"
    url_view_dataset="http://127.0.0.1:5000/view_dataset/"

    # Prepare data for POST request
    data = {
        'dataset_name': args.dataset_name,
        'summary_data_link': args.summary_data_link
    }

    # Prepare files for POST request
    raw_data_files = [('raw_data_folder', open(os.path.join(args.raw_data_folder, file), 'rb')) for file in os.listdir(args.raw_data_folder)]
    processed_data_files = [('processed_data_folder', open(os.path.join(args.processed_data_folder, file), 'rb')) for file in os.listdir(args.processed_data_folder)]


    # Combine data and files for the POST request
    whole_data  = {'dataset_name': args.dataset_name, 'summary_data_link': args.summary_data_link}
    files = raw_data_files + processed_data_files

    # Send POST request
    response = requests.post(url_add_data, data=whole_data, files=files)

    # Check the response status
    if response.status_code == 200:
        # Parse HTML content with BeautifulSoup to find the dataset name
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all <strong> elements
        strong_elements = soup.find_all('strong')
        if not strong_elements:
            print("Cannot find the dataset name. Please find the dataset manually.")
        else:
            dataset_name=[strong_element.next_sibling.strip() for strong_element in strong_elements ]
            # Create a README file with the dataset name
            dataset_path = url_view_dataset+dataset_name[-1]
            readme_content = f"This dataset is part of the data registry. For more information, visit: {dataset_path}"
            with open(os.path.join(args.dataset_folder, "README.txt"), "w") as readme_file:
                readme_file.write(readme_content)
                print(f"Data added successfully for dataset: {dataset_name[-1]}. Access the README file to get the link.")
    else:
        print(f"Failed to add data. Status code: {response.status_code}")

   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add data via command line.")
    parser.add_argument('--dataset_folder',dest='dataset_folder', required=True, help="Name of the dataset folder")
    parser.add_argument('--name', '-dn', dest='dataset_name', required=True, help="Name of the dataset")
    parser.add_argument('--raw_data_folder', '-rdf', dest='raw_data_folder', required=True, help="Path to raw data folder")
    parser.add_argument('--processed_data_folder', '-pdf', dest='processed_data_folder', required=True, help="Path to processed data folder")
    parser.add_argument('--summary_data_link', '-sdl', dest='summary_data_link', required=True, help="Summary data link")
    args = parser.parse_args()

    upload_to_registry(args)


