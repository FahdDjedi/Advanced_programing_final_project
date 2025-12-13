import requests
import csv
import io

# The VPN Gate Public API URL
API_URL = "http://www.vpngate.net/api/iphone/"

def fetch_servers():
    """
    Downloads the server list, parses CSV, and returns a list of dictionaries.
    """
    print("[*] Fetching server list from VPN Gate... (this may take a moment)")
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Check for HTTP errors
        
        # The API returns a text file with comments. We need to process it.
        # We split by newlines and remove lines starting with '*' or '#'
        data_lines = response.text.split('\n')
        
        # Find the header line (starts with #HostName) and the data following it
        start_index = 0
        for i, line in enumerate(data_lines):
            if line.startswith('#HostName'):
                start_index = i
                break
        
        # Reconstruct the CSV string starting from header
        csv_data = '\n'.join(data_lines[start_index:])
        
        # Parse CSV
        servers = []
        reader = csv.DictReader(io.StringIO(csv_data))
        
        for row in reader:
            # Check if row is valid and has OpenVPN config
            if row and 'OpenVPN_ConfigData_Base64' in row and row['OpenVPN_ConfigData_Base64']:
                servers.append({
                    'host': row['#HostName'],
                    'ip': row['IP'],
                    'country': row['CountryLong'],
                    'speed_mbps': round(int(row['Speed']) / 1000000, 2), # Convert bytes to Mbps
                    'ping': row['Ping'],
                    'config_base64': row['OpenVPN_ConfigData_Base64']
                })
                
        # Sort by speed (fastest first)
        servers.sort(key=lambda x: x['speed_mbps'], reverse=True)
        return servers

    except Exception as e:
        print(f"[!] Error fetching servers: {e}")
        return []

def get_countries(servers):
    """Returns a sorted list of unique countries available."""
    countries = set(s['country'] for s in servers)
    return sorted(list(countries))