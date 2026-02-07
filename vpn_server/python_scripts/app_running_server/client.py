import sys
import os
from tabulate import tabulate # For nice tables
import socket
import ssl
import json
import os
import random

# Ensure the parent `python_scripts` folder is on sys.path so sibling packages import correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from local_server.data import VPNData
import open_source.vpn_api as vpn_api
import open_source.vpn_core as vpn_core
import local_server.vpn_server as local_vpn_server
from server import clear_screen, service_choice_map as services

import mysql.connector
from dotenv import load_dotenv, dotenv_values

# setting up constant and the enviorenment
vpn_data = VPNData()

# set up database connection
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

database = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS
)

curser = database.cursor()

def handle_auth():
    username = input("Enter username: ")
    password = input("Enter password: ")
    curser.execute(f"USE {DB_NAME};")
    curser.execute(f"SELECT * FROM client WHERE email='{username}' AND pswrd='{password}';")
    result = curser.fetchone()
    if result:
        print("Authentication successful.")
    else:
        print("Authentication failed. Exiting.")
        sys.exit(1)
        return False
        
    return True

def local_usage(conn):
    print(conn.recv(1024).decode())
    country_choice = input("Enter your choice (1-5): ")

    while country_choice not in ['1', '2', '3', '4', '5']:
            print("Invalid choice. Please enter a number between 1 and 5 : ")
            country_choice = conn.recv(1024).decode().strip()
    
    # Send the country choice as an integer to the server
    conn.send(country_choice.encode())

    data = conn.recv(1024)
    print(f"Received from server:\n {data.decode()}")

    return

def open_usage(conn):
    servers = conn.recv(1024).decode()
    if not servers:
        print("[!] Could not retrieve servers. Exiting.")
        sys.exit(1)
    
    print(conn.recv(1024).decode())

    countries = vpn_api.get_countries(servers)
    print(conn.recv(1024).decode())

    # Display countries in columns or a simple list
    for i, country in enumerate(countries, 1):
        print(conn.recv(1024).decode())

    print(conn.recv(1024).decode())

    country_choice = input("Enter your choice (1-5 or Q to quit): ")

    while country_choice not in len(countries):
            print("Invalid choice. Please enter a number between 1 and 5 : ")
            country_choice = conn.recv(1024).decode().strip()

    if country_choice.lower() == 'q':
            print(conn.recv(1024).decode())
            run = False
            

    if not country_choice.isdigit() or int(country_choice) < 1 or int(country_choice) > len(countries):
        print(conn.recv(1024).decode())
        
    selected_country = countries[int(country_choice) - 1]
    country_servers = [s for s in servers if s['country'] == selected_country]
    table_data = []
    for i, s in enumerate(country_servers[:5], 1):
        table_data.append([i, s['ip'], f"{s['speed_mbps']} Mbps", f"{s['ping']} ms"])

    print(conn.recv(1024).decode())
    print(conn.recv(1024).decode())

    server_choice = input(f"Select server (1-{len(countries)}) or 'b' to back: ")
    conn.send(server_choice.encode())

            
    if not server_choice.isdigit() or int(server_choice) < 1 or int(server_choice) > len(table_data):
        print(conn.recv(1024).decode())
            
    # 4. Connect
    target_server = country_servers[int(server_choice) - 1]
    vpn_core.connect_openvpn(target_server['config_base64'], selected_country, target_server['ip'])
    
    # After disconnection, loop back to menu
    print(conn.recv(1024).decode())


    clear_screen()
    return


def vpn_client(host, port):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("server.crt")

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.connect((host, port))
    conn = context.wrap_socket(raw_socket, server_hostname=host)

    welcome_message = ("========================================\n"
                       "          TERMINAL VPN MANAGER          \n"
                       "========================================")
    print(welcome_message)
    print("\n")
    if sys.platform != 'win32' and os.geteuid() != 0:
        print("[!] WARNING: This script usually requires root (sudo) to manage network interfaces.")
    print("\n")
    print("\n")

    if not handle_auth():
        conn.close()
        return
    
    print("\n")
    print("\n")
    print("Select VPN Service:")
    print("1. Local Hosting")
    print("2. Open Server")

    service_choice = input("Enter your choice (1-2): ")
    while service_choice not in ['1', '2']:
        print("Invalid choice. Please enter a number between 1 and 2.")
        service_choice = input("Enter your choice (1-2): ")

    # Send the service choice as an integer to the server
    conn.send(service_choice.encode())

    if services.get(service_choice) == 'LOCAL HOSTING':
        local_usage(conn)
    elif services.get(service_choice) == 'OPEN SERVER':
        open_usage(conn)

    if input("Do you want to disconnect? (y/n): ").lower() == 'y':
        print("Disconnecting from VPN server.")
        conn.send(b'DISCONNECT')
        conn.close()

if __name__ == "__main__":
    vpn_client('127.0.0.1', 8443)