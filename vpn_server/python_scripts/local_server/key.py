"""
SSL Certificate and Key Management for VPN Server
This module handles SSL certificate generation, validation, and management.
"""

import os
import ssl
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta

class CertificateManager:
    def __init__(self):
        self.cert_file = "server.crt"
        self.key_file = "server.key"
        self.csr_file = "server.csr"
        self.config_file = "server.crt.cnf"
        
    def check_openssl_installed(self):
        """Check if OpenSSL is installed and available"""
        try:
            result = subprocess.run(['openssl', 'version'], 
                                  capture_output=True, text=True, check=True)
            print(f"OpenSSL version: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("OpenSSL not found. Please install OpenSSL to generate certificates.")
            return False
    
    def generate_private_key(self, key_size=2048):
        """Generate a private key"""
        print(f"Generating private key ({key_size} bits)...")
        try:
            cmd = [
                'openssl', 'genrsa',
                '-out', self.key_file,
                str(key_size)
            ]
            subprocess.run(cmd, check=True)
            print(f"Private key generated: {self.key_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error generating private key: {e}")
            return False
    
    def generate_csr(self, country="US", state="State", city="City", 
                    organization="VPN Server", common_name="localhost"):
        """Generate a Certificate Signing Request (CSR)"""
        print("Generating Certificate Signing Request...")
        
        # Create OpenSSL config file
        config_content = f"""[req]
            distinguished_name = req_distinguished_name
            req_extensions = v3_req
            prompt = no

            [req_distinguished_name]
            C = {country}
            ST = {state}
            L = {city}
            O = {organization}
            CN = {common_name}

            [v3_req]
            keyUsage = keyEncipherment, dataEncipherment
            extendedKeyUsage = serverAuth
            subjectAltName = @alt_names

            [alt_names]
            DNS.1 = {common_name}
            DNS.2 = localhost
            IP.1 = 127.0.0.1
            """
        
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        try:
            cmd = [
                'openssl', 'req',
                '-new',
                '-key', self.key_file,
                '-out', self.csr_file,
                '-config', self.config_file
            ]
            subprocess.run(cmd, check=True)
            print(f"CSR generated: {self.csr_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error generating CSR: {e}")
            return False
    
    def generate_self_signed_certificate(self, days=365):
        """Generate a self-signed certificate"""
        print(f"Generating self-signed certificate (valid for {days} days)...")
        try:
            cmd = [
                'openssl', 'x509',
                '-req',
                '-in', self.csr_file,
                '-signkey', self.key_file,
                '-out', self.cert_file,
                '-days', str(days),
                '-extensions', 'v3_req',
                '-extfile', self.config_file
            ]
            subprocess.run(cmd, check=True)
            print(f"Self-signed certificate generated: {self.cert_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error generating certificate: {e}")
            return False
    
    def check_certificate_validity(self):
        """Check if certificate exists and is valid"""
        if not os.path.exists(self.cert_file) or not os.path.exists(self.key_file):
            return False
        
        try:
            # Check certificate expiration
            cmd = ['openssl', 'x509', '-in', self.cert_file, '-noout', '-dates']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            print("Certificate information:")
            print(result.stdout)
            
            # Check if certificate is expired
            cmd = ['openssl', 'x509', '-in', self.cert_file, '-noout', '-checkend', '0']
            subprocess.run(cmd, check=True)
            print("Certificate is valid and not expired")
            return True
            
        except subprocess.CalledProcessError:
            print("Certificate is expired or invalid")
            return False
    
    def generate_certificates(self, force=False):
        """Generate complete SSL certificate setup"""
        print("Starting SSL certificate generation...")
        
        if not self.check_openssl_installed():
            return False
        
        # Check if certificates already exist
        if not force and self.check_certificate_validity():
            print("Valid certificates already exist. Use --force to regenerate.")
            return True
        
        # Generate private key
        if not self.generate_private_key():
            return False
        
        # Generate CSR
        if not self.generate_csr():
            return False
        
        # Generate self-signed certificate
        if not self.generate_self_signed_certificate():
            return False
        
        print("SSL certificate generation completed successfully!")
        return True
    
    def show_certificate_info(self):
        """Display certificate information"""
        if not os.path.exists(self.cert_file):
            print("Certificate file not found")
            return
        
        try:
            # Show certificate details
            cmd = ['openssl', 'x509', '-in', self.cert_file, '-text', '-noout']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("Certificate Details:")
            print(result.stdout)
            
            # Show certificate dates
            cmd = ['openssl', 'x509', '-in', self.cert_file, '-noout', '-dates']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("\nCertificate Validity:")
            print(result.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"Error reading certificate: {e}")
    
    def cleanup_certificates(self):
        """Remove certificate files"""
        files_to_remove = [self.cert_file, self.key_file, self.csr_file, self.config_file]
        removed_files = []
        
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
                removed_files.append(file)
        
        if removed_files:
            print(f"Removed files: {', '.join(removed_files)}")
        else:
            print("No certificate files found to remove")

def generate_certificates(force=False):
    """Convenience function to generate certificates"""
    manager = CertificateManager()
    return manager.generate_certificates(force)

def check_certificates():
    """Convenience function to check certificates"""
    manager = CertificateManager()
    return manager.check_certificate_validity()

def show_certificate_info():
    """Convenience function to show certificate info"""
    manager = CertificateManager()
    manager.show_certificate_info()

def main():
    """Command line interface for certificate management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSL Certificate Management for VPN Server')
    parser.add_argument('command', choices=[
        'generate', 'check', 'info', 'cleanup'
    ], help='Certificate management command')
    parser.add_argument('--force', action='store_true', 
                       help='Force regeneration of existing certificates')
    parser.add_argument('--days', type=int, default=365, 
                       help='Certificate validity in days (default: 365)')
    
    args = parser.parse_args()
    
    manager = CertificateManager()
    
    if args.command == 'generate':
        manager.generate_certificates(args.force)
    elif args.command == 'check':
        if manager.check_certificate_validity():
            print("Certificates are valid")
        else:
            print("Certificates are invalid or missing")
    elif args.command == 'info':
        manager.show_certificate_info()
    elif args.command == 'cleanup':
        manager.cleanup_certificates()

if __name__ == "__main__":
    main()