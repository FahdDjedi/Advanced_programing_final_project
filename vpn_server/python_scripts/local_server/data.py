
import random


class VPNData:
    def __init__(self):
        self.servers = {
            'FR': [
                {
                'proxy': 'http://212.83.168.126:8081',
                'protocol': 'http',
                'ip': '212.83.168.126',
                'port': 8081,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://62.138.18.91:443',
                'protocol': 'http',
                'ip': '62.138.18.91',
                'port': 443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://130.180.208.145:443',
                'protocol': 'http',
                'ip': '130.180.208.145',
                'port': 443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                }
            ],
            'JP': [
                {
                'proxy': 'http://103.37.111.253:10086',
                'protocol': 'http',
                'ip': '103.37.111.253',
                'port': 10086,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://103.241.129.239:8443',
                'protocol': 'http',
                'ip': '103.241.129.239',
                'port': 8443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://103.241.129.240:8443',
                'protocol': 'http',
                'ip': '103.241.129.240',
                'port': 8443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                }
            ],
            'US': [
                {
                'proxy': 'http://167.99.236.14:443',
                'protocol': 'http',
                'ip': '167.99.236.14',
                'port': 443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://156.146.59.33:9002',
                'protocol': 'http',
                'ip': '156.146.59.33',
                'port': 9002,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://138.199.35.211:9002',
                'protocol': 'http',
                'ip': '138.199.35.211',
                'port': 9002,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                }
            ],
            'DE': [
                {
                'proxy': 'http://87.249.132.97:9443',
                'protocol': 'http',
                'ip': '87.249.132.97',
                'port': 9443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://167.235.198.62:443',
                'protocol': 'http',
                'ip': '167.235.198.62',
                'port': 443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://94.16.116.86:8448',
                'protocol': 'http',
                'ip': '94.16.116.86',
                'port': 8448,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                }
            ],
            'GB': [
                {
                'proxy': 'http://23.106.56.43:19881',
                'protocol': 'http',
                'ip': '23.106.56.43',
                'port': 19881,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://23.106.56.35:16927',
                'protocol': 'http',
                'ip': '23.106.56.35',
                'port': 16927,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                },
                {
                'proxy': 'http://84.17.50.193:9443',
                'protocol': 'http',
                'ip': '84.17.50.193',
                'port': 9443,
                'https': True,
                'anonymity': 'transparent',
                'score': 1,
                }
            ]
    }


    def display_all_servers(self):
        print("Available VPN Servers:")
        for country, servers_list in self.servers.items():
            for server in servers_list:
                ip = server.get("ip", "Unknown")
                port = server.get("port", "Unknown")
                https_status = server['https']

                output = f' proxy: {server["proxy"]},\n protocol: {server["protocol"]},\n ip: {ip},\n port: {port},\n https: {https_status},\n anonymity: {server["anonymity"]},\n score: {server["score"]},\n country: {country}'
                print("{\n" + output +"\n}\n")


    def display_servers_by_country(self, country_code):
        country_code = country_code.upper()
        if country_code in self.servers:
            print(f"VPN Servers in {country_code}:")
            for server in self.servers[country_code]:
                ip = server.get("ip", "Unknown")
                port = server.get("port", "Unknown")
                https_status = server['https']

                output = f' proxy: {server["proxy"]},\n protocol: {server["protocol"]},\n ip: {ip},\n port: {port},\n\n https: {https_status},\n anonymity: {server["anonymity"]},\n score: {server["score"]}'
                print("{\n" + output +"\n}\n")
        else:
            print(f"No servers found for country code: {country_code}")


    def choose_server_for_country(self, country_code):
        country_code = country_code.upper()
        if country_code in self.servers:
            number = random.randint(0, len(self.servers[country_code]) - 1)
            return self.servers[country_code][number]
        else:
            print(f"No servers found for country code: {country_code}")
            return None
        
    def get_server_info(self, server):
        ip = server.get("ip", "Unknown")
        port = server.get("port", "Unknown")
        https_status = server['https']

        output = f' proxy: {server["proxy"]},\n protocol: {server["protocol"]},\n ip: {ip},\n port: {port},\n https: {https_status},\n anonymity: {server["anonymity"]},\n score: {server["score"]}'
        
        return output

if __name__ == "__main__":
    data_instance = VPNData()
    data_instance.display_all_servers()
    # Example: Display servers for a specific country
    # display_servers_by_country('US')
