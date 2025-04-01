import re
import sys
import random
import os
import requests
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# URL for the IEEE OUI file
OUI_URL = "https://standards-oui.ieee.org/oui/oui.txt"
OUI_FILE = "oui.txt"

# Function to download the OUI file
def download_oui_file():
    try:
        print(f"Downloading OUI file from {OUI_URL}...")
        response = requests.get(OUI_URL)
        response.raise_for_status()  # Check if request was successful
        with open(OUI_FILE, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("OUI file downloaded successfully.")
    except Exception as e:
        print(f"Error downloading OUI file: {e}")
        sys.exit(1)

# Load IEEE OUI database into a dictionary with UTF-8 encoding
def load_oui_database(oui_file):
    oui_dict = {}
    with open(oui_file, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
        for line in file:
            # Only process lines that contain the OUI and the organization name
            if '(hex)' in line:
                parts = line.split('(hex)')
                if len(parts) == 2:
                    oui = parts[0].strip().replace(":", "").replace("-", "").upper()
                    organization = parts[1].strip()
                    oui_dict[oui] = organization
    return oui_dict

# Function to get a random color from available colorama colors
def get_random_color():
    colors = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.RED, Fore.MAGENTA, Fore.BLUE]
    return random.choice(colors)

# Function to get OUI and Organization from MAC addresses
def get_oui_and_org(mac_addresses, oui_dict):
    oui_and_org_list = []
    org_colors = {}  # Dictionary to store organization colors

    for mac in mac_addresses:
        # Ensure that the MAC address is in a valid format (xx:xx:xx:xx:xx:xx)
        if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
            # Extract the OUI (first 3 bytes)
            oui = mac[:8].replace(":", "").replace("-", "").upper()  # Remove separators and make uppercase
            
            # Lookup the OUI in the dictionary
            organization = oui_dict.get(oui, "Organization not found")
            
            # If it's the first time encountering this organization, assign a random color
            if organization not in org_colors:
                org_colors[organization] = get_random_color()

            # Get the color for the organization
            org_color = org_colors[organization]

            # Store the OUI and organization with their respective colors
            oui_and_org_list.append((oui, organization, org_color))

        else:
            print(f"Invalid MAC address: {mac}")
    return oui_and_org_list

# Read MAC addresses from file
def read_mac_addresses_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Use UTF-8 encoding to handle all characters
            mac_addresses = file.read().splitlines()
        return mac_addresses
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

# Function to validate and collect MAC addresses from the command line
def get_mac_addresses_from_cli():
    mac_addresses = []
    for arg in sys.argv[2:]:
        # Check if each argument is a valid MAC address
        if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', arg):
            mac_addresses.append(arg)
        else:
            print(f"Invalid MAC address format: {arg}")
    return mac_addresses

if __name__ == "__main__":
    # Check if the OUI file exists, if not, download it
    if not os.path.exists(OUI_FILE):
        download_oui_file()

    if len(sys.argv) < 2:
        print("Usage: python OUIFinder.py <maclist.txt> [MAC address 1] [MAC address 2] ...")
        sys.exit(1)

    mac_addresses = []

    if os.path.exists(sys.argv[1]):  # Check if the first argument is a file
        mac_file = sys.argv[1]
        mac_addresses = read_mac_addresses_from_file(mac_file)
    else:  # If the first argument is not a file, assume MAC addresses are provided in the CLI
        mac_addresses = get_mac_addresses_from_cli()

    # Load the OUI database
    oui_dict = load_oui_database(OUI_FILE)

    # Get OUI and organization details
    oui_and_org_list = get_oui_and_org(mac_addresses, oui_dict)

    # Print results with colors
    print("OUI and Organization Names:")
    for oui, organization, org_color in oui_and_org_list:
        print(f"{Fore.YELLOW}{oui}: {org_color}{organization}")
