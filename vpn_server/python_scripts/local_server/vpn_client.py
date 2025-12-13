import socket
import ssl


def handle_auth():
    
    return True

def vpn_client(host, port):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("server.crt")

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.connect((host, port))
    conn = context.wrap_socket(raw_socket, server_hostname=host)

    print("Choose a country to connect to:")
    print("1. France")
    print("2. Germany")
    print("3. United Kingdom")
    print("4. Japan")
    print("5. United States")
    country_choice = input("Enter your choice (1-5): ")

    while country_choice not in ['1', '2', '3', '4', '5']:
        print("Invalid choice. Please enter a number between 1 and 5.")
        country_choice = input("Enter your choice (1-5): ")

    # Send the country choice as an integer to the server
    conn.send(country_choice.encode())

    data = conn.recv(1024)
    print(f"Received from server: {data.decode()}")
    
    if input("Do you want to disconnect? (y/n): ").lower() == 'y':
        print("Disconnecting from VPN server.")
        conn.send(b'DISCONNECT')
        conn.close()

if __name__ == "__main__":
    vpn_client('127.0.0.1', 8443)