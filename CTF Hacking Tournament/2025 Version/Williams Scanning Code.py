import os
import platform
import socket
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Function to get the local IP address
def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None

# Function to ping a device to check if it is online
def ping_device(ip):
    """Ping a device to check if it is online."""
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    command = f"ping {param} -w 1 {ip} > nul 2>&1" if platform.system().lower() == "windows" else f"ping {param} -W 1 {ip} > /dev/null 2>&1"
   
    return ip if os.system(command) == 0 else None

# Function to get the MAC address from ARP table
def get_mac_from_arp(ip):
    """Get the MAC address from the ARP table."""
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        for line in output.splitlines():
            if ip in line:
                mac_address = line.split()[1]
                return mac_address
    except Exception as e:
        print(f"Error getting MAC address for {ip}: {e}")
    return None

# Updated Manufacturer Database with more Raspberry Pi prefixes
OUI_DATABASE = {
    # Raspberry Pi prefixes
    "B8-27-EB": "Raspberry Pi Foundation",
    "DC-A6-32": "Raspberry Pi Foundation",
    "E4-5F-01": "Raspberry Pi Foundation",
    "28-CD-C1": "Raspberry Pi Foundation",
    "D8-3A-DD": "Raspberry Pi Foundation",
    "98-DA-60": "Raspberry Pi Foundation",
   
    # Other manufacturers
    "00-14-22": "Cisco Systems",
    "00-1A-92": "Intel Corporation",
    "00-1B-44": "Apple Inc.",
    "00-0C-29": "VMware, Inc.",
    "00-23-54": "Hewlett Packard",
    "00-1D-72": "Sony Corporation",
    "00-11-32": "Motorola Solutions",
    "00-1F-1F": "Broadcom",
    "00-60-2F": "Samsung Electronics",
    "00-15-99": "LG Electronics",
    "00-16-6F": "BenQ",
    "18-03-73": "AsusTek Computer",
    "00-1E-C2": "Hewlett Packard",
    "00-21-9B": "Xiaomi Inc.",
    "28-6A-8D": "Huawei Technologies",
    "A4-8E-5D": "Google",
    "54-16-00": "Nest Labs",
    "F8-1F-12": "Amazon Technologies",
    "00-50-56": "VMware, Inc.",
    "FC-15-B4": "Microsoft Corporation",
    "00-17-C2": "Netgear",
    "00-1C-DF": "Belkin International",
    "D4-6D-50": "TP-Link Technologies",
    "3C-2E-F9": "Aruba Networks",
    "00-26-BB": "D-Link Corporation",
    "60-A4-4C": "Dell Inc.",
    "44-65-0D": "Roku, Inc.",
    "B4-52-7E": "Google Nest",
    "F4-5C-89": "Sonos, Inc.",
    "F8-8F-CA": "Ubiquiti Networks",
    "20-CB-EB": "OnePlus Technology",
    "74-DA-38": "Nintendo Co., Ltd.",
    "00-1D-D8": "Tesla Motors",
    "D0-73-D5": "Hikvision Digital Technology",
    "10-0B-A9": "Ring LLC",
}

# Function to look up manufacturer using the offline OUI database
def get_mac_manufacturer(mac):
    """Offline lookup of manufacturer based on MAC address."""
    mac_prefix = mac[:8].upper().replace(":", "-")  # Normalize MAC address format
    return OUI_DATABASE.get(mac_prefix, "Unknown Manufacturer")

# Function to scan the network and get active devices with their MAC addresses
def scan_network(network):
    """Scan the local network for active devices."""
    devices = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping_device, [str(ip) for ip in ipaddress.IPv4Network(network, strict=False)])
   
    for ip in results:
        if ip:
            mac_address = get_mac_from_arp(ip)
            if mac_address:
                manufacturer = get_mac_manufacturer(mac_address)
                devices.append({"ip": ip, "mac": mac_address, "manufacturer": manufacturer})

    return devices

if __name__ == "__main__":
    local_ip = get_local_ip()
    if local_ip:
        network_prefix = ".".join(local_ip.split(".")[:-1]) + ".0/24"  # Assuming a /24 subnet
        print(f"Scanning network: {network_prefix}")

        devices = scan_network(network_prefix)
        print("\nActive Devices:")
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}, Manufacturer: {device['manufacturer']}")
    else:
        print("Could not determine local IP.")