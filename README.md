# OUI Finder

This Python script helps you find the organization associated with a given MAC address by using the IEEE Organizationally Unique Identifier (OUI) database. The script will either read a list of MAC addresses from a file or from command-line arguments and then return the corresponding organization names for those addresses. It fetches the OUI data from the IEEE OUI standard file and utilizes the `colorama` library to print the results in different colors for easy distinction.

## Features

- Downloads the IEEE OUI text file from the official URL if not present locally.
- Parses the OUI database and retrieves the organization name for a given MAC address.
- Accepts MAC addresses as command-line arguments or from a text file.
- Displays the results in colorful format for better readability.
- Ensures that only valid MAC addresses are processed.

## Requirements

- Python 3.x
- `requests` library
- `colorama` library

You can install the required libraries using `pip`:

```bash
pip install requests colorama
```

## Usage

### 1. Command Line Usage

You can either provide a list of MAC addresses directly in the command line or provide a file containing the MAC addresses. The script will check if the first argument is a file. If it's a file, it will read the MAC addresses from it; otherwise, it will treat the arguments as MAC addresses.

```bash
python OUIFinder.py <maclist.txt> [MAC address 1] [MAC address 2] ...
```

- `<maclist.txt>`: A file containing a list of MAC addresses (one per line).
- `[MAC address 1] [MAC address 2] ...`: A list of MAC addresses passed as command-line arguments.

### 2. Example Usage

To run the script with a MAC address file:

```bash
python OUIFinder.py maclist.txt
```

To run the script with MAC addresses passed as arguments:

```bash
python OUIFinder.py 00:14:22:01:23:45 00:50:56:A1:B2:C3
```

### 3. Output

The script will display the OUI (first 3 bytes of the MAC address) and the corresponding organization name for each valid MAC address. The results will be color-coded to distinguish between organizations.

Example output:

```bash
OUI and Organization Names:
00:14:22: VMware, Inc.
00:50:56: Cisco Systems, Inc
```

## Script Breakdown

### `download_oui_file()`
Downloads the IEEE OUI file from the official IEEE website and saves it locally as `oui.txt`.

### `load_oui_database(oui_file)`
Loads the OUI data from the local `oui.txt` file into a dictionary. The key is the OUI (first 3 bytes of the MAC address), and the value is the organization name.

### `get_random_color()`
Returns a random color from the available colors in the `colorama.Fore` module to be used for displaying the organization name in different colors.

### `get_oui_and_org(mac_addresses, oui_dict)`
Processes a list of MAC addresses and looks up the organization name associated with each address using the OUI dictionary. It assigns a color to each organization and returns the results.

### `read_mac_addresses_from_file(file_path)`
Reads MAC addresses from a text file, one address per line.

### `get_mac_addresses_from_cli()`
Validates and collects MAC addresses passed as command-line arguments.

## Error Handling

- The script will display an error message and exit if the `oui.txt` file cannot be downloaded.
- If the input file does not exist or cannot be read, an appropriate error message will be shown.
- Invalid MAC addresses are ignored, and a message will indicate which addresses are not valid.

