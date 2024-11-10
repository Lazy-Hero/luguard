import vpndpi
import colorama
from colorama import Fore, Style
import cfgen
import subprocess
import os
import ctypes


colorama.init(autoreset=True)
author_name = "https://t.me/shalopaybase"

def config_create():
    warp = cfgen.CloudflareWarp()
    warp.run()

def dpi_crash():
    parsing_conf()
    vpndpi.dpi_crasher(None, lsport)

def auto_spoof():
    print(f"Settings get...")
    parsing_conf()
    if auto_send:
        vpndpi.dpi_crasher(lsport, None)
    if auto_connect:
        if is_admin():
            install_wireguard_tunnel(f"{os.getcwd()}/cfwarp.conf")
        else:
            print(Fore.RED + "!!!Run the program with administrator rights to automatically connect to the tunnel!!!")

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    return False

def install_wireguard_tunnel(config_path):
    try:
        command = ["wireguard.exe", "/installtunnelservice", config_path]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Tunnel service installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error occurred while installing tunnel service.")

def uninstall_wireguard_tunnel(config_name):
    try:
        command = ["wireguard.exe", "/uninstalltunnelservice", config_name]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Tunnel service installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error occurred while installing tunnel service.")


def parsing_conf():
    with open('settings.cfg', 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if value.lower() == 'true':
                    globals()[key] = True
                elif value.lower() == 'false':
                    globals()[key] = False
                else:
                    try:
                        globals()[key] = int(value)
                    except ValueError:
                        globals()[key] = value

def display_menu():
    print(Fore.YELLOW + f"\nLuGuard Developer: {Style.BRIGHT + Fore.WHITE}{author_name}\n")
    print(Fore.MAGENTA + "Select an option:")
    print(Fore.WHITE + "1. Generate config for Wireguard")
    print(Fore.WHITE + "2. Send fake packets to the Wireguard port")
    print(Fore.WHITE + "3. Use automatic configuration file [settings.cfg]")
    print(Fore.WHITE + "0. Exit")

def main():
    while True:
        display_menu()
        choice = input(Fore.YELLOW + "\nEnter the option number: ")

        if choice == '1':
            config_create()
        elif choice == '2':
            dpi_crash()
        elif choice == '3':
            auto_spoof()
        elif choice == '0':
            print(Fore.GREEN + "Exiting the program...")
            break
        else:
            print(Fore.RED + "Wrong choice, try again.")

if __name__ == "__main__":
    main()