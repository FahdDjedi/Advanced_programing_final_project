import base64
import subprocess
import tempfile
import os
import sys
import signal

def connect_openvpn(config_base64, country, ip):
    """
    Decodes the config, creates a temp file, and runs OpenVPN.
    """
    print(f"\n[*] Preparing to connect to {country} ({ip})...")
    
    # 1. Decode the Base64 Config provided by the API
    try:
        config_content = base64.b64decode(config_base64).decode('utf-8')

        config_content += "\n"
        config_content += "data-ciphers AES-256-GCM:AES-128-GCM:AES-256-CBC:AES-128-CBC\n"
        config_content += "data-ciphers-fallback AES-128-CBC\n"
    except Exception as e:
        print(f"[!] Error decoding configuration: {e}")
        return

    # 2. Create a temporary .ovpn file
    # OpenVPN needs a physical file to read the configuration from
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ovpn', delete=False) as temp_config:
        temp_config.write(config_content)
        temp_config_path = temp_config.name

    print(f"[*] Configuration loaded. Launching OpenVPN Engine...")
    print("[*] Press CTRL+C to disconnect.\n")

    # 3. Construct the command
    # We need 'sudo' on Linux/Mac because VPNs modify network interfaces
    command = []
    
    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        command = ['sudo', 'openvpn', '--config', temp_config_path]
    elif sys.platform.startswith('win'):
        # On Windows, user must run the Python script as Administrator
        command = ['openvpn', '--config', temp_config_path]
    
    process = None
    try:
        # 4. Start the process
        # We pipe stdout to sys.stdout so the user sees the OpenVPN logs
        process = subprocess.Popen(command)
        process.wait() # This line blocks the code here until OpenVPN exits
        
    except KeyboardInterrupt:
        # Handle CTRL+C cleanly
        print("\n\n[!] User requested disconnect.")
    except FileNotFoundError:
        print("\n[!] ERROR: 'openvpn' command not found.")
        print("    Please install OpenVPN and ensure it's in your system PATH.")
    finally:
        # 5. Cleanup
        if process and process.poll() is None:
            print("[*] Terminating OpenVPN process...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        # Remove the temp file
        if os.path.exists(temp_config_path):
            os.remove(temp_config_path)
        print("[*] Disconnected. Temporary config deleted.")