import requests
import json
from datetime import datetime, timezone
from wireguard_tools import WireguardKey
import random
import colorama
from colorama import Fore, Style
import os

colorama.init(autoreset=True)

hook_port = 0

class CloudflareWarp:
    def __init__(self):
        self.private_key = WireguardKey.generate()
        self.public_key = self.private_key.public_key()
        self.random_port = random.randint(51000, 51200)
        self.api = "https://api.cloudflareclient.com/v0i1909051800"
        self.proxy_use = False
        self.proxies = {}

    def set_proxies(self, proxy_dict):
        self.proxies = {
            "http": f"{proxy_dict}",
            "https": f"{proxy_dict}"
        }

    def ins(self, method, endpoint, headers=None, data=None):
        url = f"{self.api}/{endpoint}"
        try:
            if not self.proxy_use:
                response = requests.request(method, url, headers=headers, data=data)
            else:
                response = requests.request(method, url, headers=headers, data=data, proxies=self.proxies)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Ошибка при выполнении запроса: {e}")
            return None

    def sec(self, method, endpoint, token, headers=None, data=None):
        auth_header = {"Authorization": f"Bearer {token}"}
        headers = headers or {}
        headers.update(auth_header)
        return self.ins(method, endpoint, headers=headers, data=data)

    def register_device(self):
        tos_date = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        data = {
            "install_id": "",
            "tos": tos_date,
            "key": str(self.public_key),
            "fcm_token": "",
            "type": "ios",
            "locale": "en_US"
        }

        response = self.ins("POST", "reg", data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response:
            return response.get('result', {})
        return {}

    def create_config(self, private_key, public_key, interface_addresses_v4, interface_addresses_v6, endpoint_host):
        config = {
            'Interface': {
                'PrivateKey': private_key,
                'Address': f"{interface_addresses_v4}/32, {interface_addresses_v6}/128",
                'ListenPort': str(self.random_port),
                'DNS': '1.1.1.1'
            },
            'Peer': {
                'PublicKey': public_key,
                'AllowedIPs': '0.0.0.0/0, ::/0',
                'Endpoint': endpoint_host
            }
        }

        with open('cfwarp.conf', 'w') as configfile:
            for section, settings in config.items():
                configfile.write(f"[{section}]\n")
                for key, value in settings.items():
                    configfile.write(f"{key} = {value}\n")
                configfile.write("\n")
        global hook_port
        hook_port = self.random_port
        print(f"{Style.BRIGHT + Fore.CYAN}Crack port: {hook_port}")
        print("Файл конфигурации cfwarp.conf успешно создан.")

    def create_setting(self):

        config = {
            'Settings' : {
                'auto_connect' : 'true',
                'auto_send' : 'true',
                'lsport' : hook_port
            }
        }
        with open('settings.cfg', 'w') as configfile:
            for section, settings in config.items():
                for key, value in settings.items():
                    configfile.write(f"{key} = {value}\n")
                configfile.write("\n")
        # os.system('cls' if os.name == 'nt' else 'clear')
        print("Файл конфигурации settings.cfg успешно создан.")

    def run(self):
        proxy_choice = input(Fore.YELLOW + f"\nИспользовать прокси для регистраций Warp? {Fore.WHITE}[Yes/no]: ").strip().lower() or 'yes'
        autospoof_choice = input(Fore.YELLOW + f"\nГенерировать settings.cfg для автоматической загрузки? {Fore.WHITE}[Yes/no]: ").strip().lower() or 'yes'
        if proxy_choice == 'yes':
            proxy_dict = self.get_proxy_dict() 
            self.set_proxies(proxy_dict)
            self.proxy_use = True


        device_data = self.register_device()
        if device_data:
            public_key_res = device_data['config']['peers'][0]['public_key']
            endpoint_host = device_data['config']['peers'][0]['endpoint']['host']
            interface_addresses_v4 = device_data['config']['interface']['addresses']['v4']
            interface_addresses_v6 = device_data['config']['interface']['addresses']['v6']
            self.create_config(self.private_key, public_key_res, interface_addresses_v4, interface_addresses_v6, endpoint_host)
            # генерация конфига для автоматической отправки спуф пакетов.
            if autospoof_choice == "yes":
                self.create_setting()

    def get_proxy_dict(self):
        import parser
        return parser.get_proxy_dict()

if __name__ == "__main__":
    warp = CloudflareWarp()
    warp.run()