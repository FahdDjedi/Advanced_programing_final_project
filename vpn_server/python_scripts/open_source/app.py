import sys
import os
from tabulate import tabulate # For nice tables
import vpn_api
import vpn_core

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Check for root/admin (Optional but recommended check)
    if sys.platform != 'win32' and os.geteuid() != 0:
        print("[!] WARNING: This script usually requires root (sudo) to manage network interfaces.")
    
    clear_screen()
    print("========================================")
    print("          TERMINAL VPN MANAGER          ")
    print("========================================")

    # 1. Fetch Servers
    servers = vpn_api.fetch_servers()
    if not servers:
        print("[!] Could not retrieve servers. Exiting.")
        sys.exit(1)

    print(f"[*] Successfully loaded {len(servers)} servers.")
    
    while True:
        # 2. Country Selection
        countries = vpn_api.get_countries(servers)
        
        print("\nAvailable Countries:")
        # Display countries in columns or a simple list
        for i, country in enumerate(countries, 1):
            print(f"{i}. {country}")
        print("Q. Quit")

        choice = input("\nSelect a country number: ").strip()
        
        if choice.lower() == 'q':
            print("Goodbye!")
            break

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(countries):
            print("[!] Invalid selection.")
            continue # continue statement makes the loop start over

        selected_country = countries[int(choice) - 1]
        
        # 3. Server Selection Logic
        # Filter servers for this country
        country_servers = [s for s in servers if s['country'] == selected_country]
        
        # Show top 5 fastest servers for this country
        print(f"\nTop Servers in {selected_country}:")
        table_data = []
        for i, s in enumerate(country_servers[:5], 1):
            table_data.append([i, s['ip'], f"{s['speed_mbps']} Mbps", f"{s['ping']} ms"])
            
        print(tabulate(table_data, headers=["ID", "IP Address", "Speed", "Ping"], tablefmt="grid"))
        
        server_choice = input(f"\nSelect server (1-{len(table_data)}) or 'b' to back: ").strip()
        
        if server_choice.lower() == 'b':
            continue
            
        if not server_choice.isdigit() or int(server_choice) < 1 or int(server_choice) > len(table_data):
            print("[!] Invalid server selection.")
            continue
            
        # 4. Connect
        target_server = country_servers[int(server_choice) - 1]
        vpn_core.connect_openvpn(target_server['config_base64'], selected_country, target_server['ip'])
        
        # After disconnection, loop back to menu
        input("\nPress Enter to return to menu...")
        clear_screen()

if __name__ == "__main__":
    main()