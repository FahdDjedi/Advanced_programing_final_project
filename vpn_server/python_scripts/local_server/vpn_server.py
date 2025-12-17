import socket
import ssl
import json
import os
import random

from data import VPNData

vpn_data = VPNData()


def start_vpn_server(host, port):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    bindsocket = socket.socket()
    bindsocket.bind((host, port))
    bindsocket.listen(5)

    print(f"VPN server listening on {host}:{port}")

    while True:
        newsocket, fromaddr = bindsocket.accept()
        print(f"Connection from {fromaddr}")
        conn = context.wrap_socket(newsocket, server_side=True)
        try:
            data = conn.recv(1024).decode()
            print(f"Received country choice: {data}")

            country_map = {
                '1': 'FR',
                '2': 'GB',
                '3': 'DE',
                '4': 'JP',
                '5': 'US'
            }
            selected_country = country_map.get(data, 'Unknown')
            print(f"Client wants to connect to: ----{selected_country}-----")

            if data:
                response_message = f"Connecting you to --{selected_country}--"
                server = vpn_data.choose_server_for_country(selected_country)
                if server:
                    response_message += f" Server details : \n {vpn_data.get_server_info(server)}"
                    print("client successfully connected to server")
                else:
                    response_message += " No server available."
                conn.sendall(response_message.encode())
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
            

if __name__ == "__main__":
    start_vpn_server('127.0.0.1', 8443)