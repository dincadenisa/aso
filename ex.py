import os
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Functie pentru a trimite ping si verifica daca o masina este activa
def ping(ip):
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    command = f"ping {param} -w 1 {ip} > /dev/null 2>&1"
    return os.system(command) == 0

# Functie pentru scanarea tuturor adreselor dintr-o subretea
def scan_subnet(subnet):
    active_ips = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping, f"{subnet}.{i}"): i for i in range(1, 255)}
        for future in futures:
            ip_suffix = futures[future]
            if future.result():
                active_ips.append(f"{subnet}.{ip_suffix}")
    return active_ips

if __name__ == "__main__":
    # Specifica subrețeaua VLAN-ului (de ex. "10.11.14")
    vlan_subnet = "10.11.14"

    print(f"Scanare pentru dispozitive active în VLAN {vlan_subnet}.0/24...")
    active_devices = scan_subnet(vlan_subnet)

    if active_devices:
        print("Dispozitive active găsite:")
        for ip in active_devices:
            print(ip)
    else:
        print("Nu s-au găsit dispozitive active în VLAN-ul specificat.")

