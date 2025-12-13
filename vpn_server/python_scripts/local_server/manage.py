#!/usr/bin/env python3
"""
VPN Server Management Script
This script provides various management commands for the VPN server.
"""

import os
import sys
import argparse
import subprocess
import signal
import time
from pathlib import Path
import threading

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vpn_server import start_vpn_server
from key import generate_certificates, check_certificates

class VPNServerManager:
    def __init__(self):
        self.server_process = None
        self.server_host = '127.0.0.1'
        self.server_port = 8443
        
    def start_server(self, host=None, port=None, background=False):
        """Start the VPN server"""
        if host:
            self.server_host = host
        if port:
            self.server_port = port
            
        print(f"Starting VPN server on {self.server_host}:{self.server_port}")
        
        if background:
            # Start server in background
            server_thread = threading.Thread(
                target=start_vpn_server, 
                args=(self.server_host, self.server_port)
            )
            server_thread.daemon = True
            server_thread.start()
            print("VPN server started in background")
            return server_thread
        else:
            # Start server in foreground
            try:
                start_vpn_server(self.server_host, self.server_port)
            except KeyboardInterrupt:
                print("\nShutting down VPN server...")
                self.stop_server()
    
    def stop_server(self):
        """Stop the VPN server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            print("VPN server stopped")
        else:
            print("No VPN server process found")
    
    def restart_server(self, host=None, port=None):
        """Restart the VPN server"""
        print("Restarting VPN server...")
        self.stop_server()
        time.sleep(2)
        self.start_server(host, port)
    
    def check_server_status(self):
        """Check if the VPN server is running"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.server_host, self.server_port))
            sock.close()
            if result == 0:
                print(f"VPN server is running on {self.server_host}:{self.server_port}")
                return True
            else:
                print(f"VPN server is not running on {self.server_host}:{self.server_port}")
                return False
        except Exception as e:
            print(f"Error checking server status: {e}")
            return False
    
    def show_logs(self, lines=50):
        """Show recent server logs"""
        print(f"Showing last {lines} lines of server logs...")
        # This is a placeholder - in a real implementation, you'd read from log files
        print("Log functionality not implemented yet")
    
    def setup_environment(self):
        """Set up the VPN server environment"""
        print("Setting up VPN server environment...")
        
        # Check if certificates exist
        if not check_certificates():
            print("Certificates not found. Generating new certificates...")
            generate_certificates()
        
        # Create necessary directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("config", exist_ok=True)
        
        print("Environment setup complete!")
    
    def show_help(self):
        """Show help information"""
        help_text = """
        -------------------------------------------------------------------------------------------------------------------------



        ===================================VPN SERVER MANAGEMENT COMMANDS :===================================================

            1. Start Server:
            python manage.py start [--host HOST] [--port PORT] [--background]

            2. Stop Server:
            python manage.py stop

            3. Restart Server:
            python manage.py restart [--host HOST] [--port PORT]

            4. Check Status:
            python manage.py status

            5. Setup Environment:
            python manage.py setup

            6. Generate Certificates:
            python manage.py certs

            7. Show Logs:
            python manage.py logs [--lines N]

            8. Show Help:
            python manage.py help

            Examples:
            python manage.py start --host 0.0.0.0 --port 8443
            python manage.py start --background
            python manage.py status
            python manage.py setup
            python manage.py certs
            python manage.py logs --lines 100

        =========================================================================================================================

            


        -------------------------------------------------------------------------------------------------------------------------
        """
        print(help_text)

    def country_choice(self):
        country_choice = """
        =========================================================================================================================


            the country available in our vpn servers are for now :
                1- France
                2- Germany
                3- Spain
                4- United Kingdom
                5- NetherLand



        =========================================================================================================================
        """
        


def main():
    parser = argparse.ArgumentParser(description='VPN Server Management Tool')

    parser.add_argument('command', choices=[
        'start', 'stop', 'restart', 'status', 'setup', 'certs', 'logs', 'help'
    ], help='Management command to execute')
    
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8443, help='Server port (default: 8443)')
    parser.add_argument('--background', action='store_true', help='Run server in background')
    parser.add_argument('--lines', type=int, default=50, help='Number of log lines to show')
    
    args = parser.parse_args()
    
    manager = VPNServerManager()
    
    if args.command == 'start':
        manager.start_server(args.host, args.port, args.background)
    elif args.command == 'stop':
        manager.stop_server()
    elif args.command == 'restart':
        manager.restart_server(args.host, args.port)
    elif args.command == 'status':
        manager.check_server_status()
    elif args.command == 'setup':
        manager.setup_environment()
    elif args.command == 'certs':
        generate_certificates()
    elif args.command == 'logs':
        manager.show_logs(args.lines)
    elif args.command == 'help':
        manager.show_help()

if __name__ == "__main__":
    main()
