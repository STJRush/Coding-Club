from scapy.all import ARP, Ether, srp
import socket
import requests

# Raspberry Pi MAC Address Prefixes (OUIs)
RASPBERRY_PI_OUIS = ["B8:27:EB", "DC:A6:32"]

def get_local_network():
    """Determine the local network IP range."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = ".".join(local_ip.split(".")[:3]) + ".0/24"
        return subnet
    except:
        return "192.168.1.0/24"  # Default fallback

def get_mac_vendor(mac_address):
    """Fetch manufacturer details from macvendors API."""
    try:
        response = requests.get(f"https://api.macvendors.com/{mac_address}", timeout=3)
        return response.text if response.status_code == 200 else "Unknown"
    except:
        return "Unknown"

def scan_network(network):
    """Scan the network for active IPs and MAC addresses."""
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in result:
        mac = received.hwsrc.upper()
        vendor = get_mac_vendor(mac)
        is_raspberry_pi = any(mac.startswith(oui) for oui in RASPBERRY_PI_OUIS)
        devices.append((received.psrc, mac, vendor, is_raspberry_pi))

    return devices

if __name__ == "__main__":
    network = get_local_network()
    print(f"Scanning network: {network}...\n")

    devices = scan_network(network)

    print("IP Address\t\tMAC Address\t\tManufacturer\t\tRaspberry Pi")
    print("="*80)
    for ip, mac, vendor, is_raspberry_pi in devices:
        pi_status = "✅ YES" if is_raspberry_pi else "❌ NO"
        print(f"{ip}\t{mac}\t{vendor}\t{pi_status}")
