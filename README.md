# Advanced_Programing_Project

Content of the project :
  this project is aiming to create a vpn server that the user can connect to via commande lines using cmd and it will be developed using python exclusivly with the objective of learning said coding language during the Adavnced Programing mudulus 
  
  This creates a learning-focused VPN server project that demonstrates networking, 
  security and Python development concepts

The spets necessary :
  1. - Setting Up the Environment
     - installing all requiered programs
     - important files to creat and write (Cly.py, Manage.py, config.py, keys.py, System.py ...)
  2. - figuring out the VPN Server Program
  3. - writing and optimizing the VPN Server Program
     - keys generating program
     - CSR (Certificate Signing Resquest) creation
     - generate a self-signed certificate
     - add unit tests, logging, error handling. Add docs and examples
     - add simple revoke/remove-peer flow and rotation notes
  4. - figuring out the VPN Client Program
  5. - writing and optimizing the VPN Client Program
  6. - test running and making sure everything is in place 
  7. - connecting to a chosen server to mark the unooficial end of the project
  8. - designing a small simple and intuitive UI to make the use of the app easier
  9. - OFFICIALLY ending and closing the project



VPN SERVER PROJECT FILES OVERVIEW:

PYTHON SCRIPTS (python_scripts/ folder):

1. vpn_server.py
   - Purpose: Main VPN server implementation
   - Function: Creates SSL-enabled server that listens for client connections
   - Key Features: SSL/TLS encryption, connection handling, data transmission

2. vpn_client.py
   - Purpose: VPN client application
   - Function: Connects to the VPN server securely
   - Key Features: SSL connection, data exchange with server

3. manage.py
   - Purpose: Server management tool
   - Function: Command-line interface for starting/stopping/managing the server
   - Key Features: Server control, status checking, environment setup

4. key.py
   - Purpose: SSL certificate management
   - Function: Generates, validates, and manages SSL certificates
   - Key Features: Certificate generation, validation, cleanup

5. config.py
   - Purpose: Configuration management
   - Function: Centralized settings for server, SSL, logging, security
   - Key Features: Environment-specific configs, validation, file management

SSL CERTIFICATE FILES:

6. server.csr.cnf
   - Purpose: OpenSSL configuration for Certificate Signing Request
   - Function: Defines certificate parameters (CN=127.0.0.1, SAN IP=127.0.0.1)
   - Key Features: Localhost certificate configuration, Subject Alternative Names

7. server.csr
   - Purpose: Certificate Signing Request file
   - Function: Request for SSL certificate from Certificate Authority
   - Key Features: Contains public key and certificate details

8. server.crt.cnf
   - Purpose: Certificate configuration file
   - Function: Settings for generating self-signed certificates
   - Key Features: Certificate extensions, key usage, subject alternative names

PROJECT STRUCTURE:
VPN_Server/
├── python_scripts/          # Main application code
│   ├── vpn_server.py       # Core server implementation
│   ├── vpn_client.py       # Client application
│   ├── manage.py           # Management interface
│   ├── key.py              # Certificate management
│   └── config.py           # Configuration settings
├── server.csr.cnf          # CSR configuration
├── server.csr              # Certificate signing request
└── server.crt.cnf          # Certificate configuration

HOW FILES WORK TOGETHER:
1. config.py → Provides settings for all other components
2. key.py → Generates SSL certificates using server.csr.cnf
3. manage.py → Uses config to start/stop the server
4. vpn_server.py → Uses certificates from key.py for secure connections
5. vpn_client.py → Connects to server using same certificate chain

PROJECT GOAL:
Build a complete Python-based VPN solution with:
- Secure SSL/TLS connections
- Command-line management
- Certificate management
- Configurable settings
- Professional structure

dEFINITIONS :
- A CSR (Certificate Signing Request) is a file you generate when you want a certificate from a Certificate Authority. it's created: generated using your private key and signed with that same private key to prove you control it. the "server.csr.cnt" sets fields like CN=127.0.0.1 and SAN IP=127.0.0.1, so the issued server certificate will be valid for localhost


The members :
  Djedi Fahd
  Angar Yacine
  Djebbar Seddik Adel
  Banazza Mehdi
