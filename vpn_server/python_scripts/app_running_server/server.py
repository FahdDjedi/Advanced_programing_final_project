import sys
import os
from tabulate import tabulate # For nice tables
import socket
import ssl
import json
import os
import random

from local_server.data import VPNData
import open_source.vpn_api as vpn_api
import open_source.vpn_core as vpn_core
import local_server.vpn_server as local_vpn_server

import mysql.connector
from dotenv import load_dotenv, dotenv_values

# setting up constant and the enviorenment
vpn_data = VPNData()
local_host, local_port = '127.0.0.1', 8443

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

# create service choice map from data base
service_choice_map = {}
curser.execute(f"USE {DB_NAME};")
curser.execute("SELECT * FROM services;")
result = curser.fetchall()
for row in result:
    service_choice_map[str(row[0])] = row[1]

# create country choice map from data base
country_map = {}
curser.execute(f"USE {DB_NAME};")
curser.execute("SELECT * FROM countries;")
result = curser.fetchall()
for row in result:
    country_map[str(row[0])] = row[1]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def local_exec(conn, run):
    try:
        conn.sendall("Choose a country to connect to: \n"
                        "1. France \n"
                        "2. Germany \n"
                        "3. United Kingdom \n"
                        "4. Japan \n"
                        "5. United States \n"
                        "Q. Quit \n".encode())

        country_choice = conn.recv(1024).decode().strip()

        # Send the country choice as an integer to the server
        print(f"Received country choice: {country_choice}")

        selected_country = country_map.get(country_choice, 'Unknown')
        print(f"Client wants to connect to: ----{selected_country}-----")

        if country_choice:
            response_message = f"Connecting you to --{selected_country}--"
            server = vpn_data.choose_server_for_country(selected_country)
            if server:
                response_message += f" Server details : \n {vpn_data.get_server_info(server)}"
                print("client successfully connected to server")
            else:
                response_message += " No server available."
            conn.sendall(response_message.encode())
        elif country_choice.lower() == 'q':
            print("client is disconnecting!")
            conn.sendall(b"Goodbye!")
            run = False
            return

    except Exception as e:
        print(f"Error: {e}")
    finally:
        run = False

    return

def open_exec(conn, run):
    clear_screen()

    # 1. Fetch Servers
    servers = vpn_api.fetch_servers()
    conn.sendall(servers.encode())
    if not servers:
        print("[!] Could not retrieve servers. Exiting.")
        sys.exit(1)

    print(f"[*] Successfully loaded {len(servers)} servers.")
    conn.sendall(f"[*] Successfully loaded {len(servers)} servers.".encode())

    while True:
        # 2. Country Selection
        countries = vpn_api.get_countries(servers)
        
        print("\nAvailable Countries:")
        conn.sendall("\nAvailable Countries: \n".encode())

        # Display countries in columns or a simple list
        for i, country in enumerate(countries, 1):
            print(f"{i}. {country}")
            conn.sendall(f"{i}. {country}\n".encode())

        conn.sendall("Q. Quit\n".encode())
        print("Q. Quit")

        choice = conn.recv(1024).decode().strip()
        
        if choice.lower() == 'q':
            print("client is disconnecting!")
            conn.sendall(b"Goodbye!")
            run = False
            break

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(countries):
            print("[!] Invalid selection.")
            conn.sendall(b"[!] Invalid selection.")
            continue # continue statement makes the loop start over

        selected_country = countries[int(choice) - 1]
        
        # 3. Server Selection Logic
        # Filter servers for this country
        country_servers = [s for s in servers if s['country'] == selected_country]
        
        # Show top 5 fastest servers for this country
        print(f"\nTop Servers in {selected_country}:")
        conn.sendall(f"\nTop Servers in {selected_country}:\n".encode())

        table_data = []
        for i, s in enumerate(country_servers[:5], 1):
            table_data.append([i, s['ip'], f"{s['speed_mbps']} Mbps", f"{s['ping']} ms"])
            
        print(tabulate(table_data, headers=["ID", "IP Address", "Speed", "Ping"], tablefmt="grid"))
        conn.sendall(tabulate(table_data, headers=["ID", "IP Address", "Speed", "Ping"], tablefmt="grid").encode())
        
        server_choice = conn.recv(1024).decode().strip()
        
        if server_choice.lower() == 'b':
            continue
            
        if not server_choice.isdigit() or int(server_choice) < 1 or int(server_choice) > len(table_data):
            print("[!] Invalid server selection.")
            conn.sendall(b"[!] Invalid server selection.")
            continue
            
        # 4. Connect
        target_server = country_servers[int(server_choice) - 1]
        vpn_core.connect_openvpn(target_server['config_base64'], selected_country, target_server['ip'])
        
        # After disconnection, loop back to menu
        conn.sendall("\nPress Enter to return to menu...".encode())
        data = conn.recv(1024).decode()

        if data == '\n' or data == '':
            run = False

        clear_screen()
    return

def main():
    run = True

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    bindsocket = socket.socket()
    bindsocket.bind((local_host, local_port))
    bindsocket.listen(5)

    print(f"VPN server listening on {local_host}:{local_port}")

    while run:
        newsocket, fromaddr = bindsocket.accept()
        print(f"Connection from {fromaddr}")
        conn = context.wrap_socket(newsocket, server_side=True)
        try:
            data = conn.recv(1024).decode()
            print(f"Received service choice: {data}")

            selected_service = service_choice_map.get(data, 'UNKNOWN')
            print(f"Client selected service: {selected_service}")

            if selected_service == 'LOCAL HOSTING':
                local_exec(conn, run)
            elif selected_service == 'OPEN SERVER':
                open_exec(conn, run)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            try:
                disconnect_message = conn.recv(1024).decode()
                if disconnect_message == 'DISCONNECT':
                    print("Client requested disconnection.")
                    conn.close()
                    print(f"Connection from {fromaddr} closed")
                    conn.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                print(f"Error during shutdown: {e}")
    
    return
            

if __name__ == "__main__":
    main()