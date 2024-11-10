import socket
import dns.resolver
import colorama
from colorama import Fore, Style
import os

def dpi_crasher(spport, cfgport):
    wg_listen_port = spport
    if spport == None:
        os.system('cls' if os.name == 'nt' else 'clear')
        wg_listen_port = input(Fore.YELLOW +f'Enter the port for the crack or press enter ({Fore.RED}{cfgport}{Fore.YELLOW}): ') or cfgport
    wg_ip = "engage.cloudflareclient.com"
    wg_port = 2408


    resolver = dns.resolver.Resolver()
    answers = resolver.resolve(wg_ip)
    ip_address = answers[0].address

    

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', int(wg_listen_port)))


    print(f"Port {Style.BRIGHT + Fore.WHITE}{int(wg_listen_port)} successfully unblocked!")
    message = b"Client Hello"
    for i in range(10):
        sock.sendto(message, (ip_address, wg_port))

    sock.close()