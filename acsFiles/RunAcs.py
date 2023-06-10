import json
import requests
from requests.exceptions import Timeout

# Load the JSON file
with open('acs.json') as file:
    data = json.load(file)

# Extract IP addresses and construct the files_server URLs
ip_addresses = []
files_server = []

for obj in data:
    ip = obj['ip']
    ip_addresses.append(ip)
    files_server.append(f"{ip}:7557/files")

# Print the IP addresses and files_server URLs
for ip, server_url in zip(ip_addresses, files_server):
    print("IP Address:", ip)
    print("Files Server URL:", server_url)

    try:
        # Fetch JSON data with timeout
        response = requests.get(f"http://{server_url}", timeout=10)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = response.json()

        # Download files
        for item in data:
            filename = item['filename']
            file_url = f"http://{ip}:7567/{filename}"
            print(f"Downloading file: {filename}")
            
            try:
                # Download each file with timeout
                response = requests.get(file_url, timeout=10)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"File downloaded: {filename}")
            
            except Timeout:
                error_message = f"Timeout occurred while downloading file: {filename}\n"
                with open("errors.txt", "a") as error_file:
                    error_file.write(error_message)
            
            except requests.exceptions.RequestException as e:
                error_message = f"Error occurred while downloading file: {filename} - {str(e)}\n"
                with open("errors.txt", "a") as error_file:
                    error_file.write(error_message)
            
            print()

    except Timeout:
        error_message = "Timeout occurred while fetching data\n"
        with open("errors.txt", "a") as error_file:
            error_file.write(error_message)
        print()
    
    except requests.exceptions.RequestException as e:
        error_message = f"Error occurred while fetching data: {str(e)}\n"
        with open("errors.txt", "a") as error_file:
            error_file.write(error_message)
        print()
