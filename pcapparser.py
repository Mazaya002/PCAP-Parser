#PYTHON PCAP PARSER PROTO
from scapy.all import rdpcap
import csv
import os

def bytes_to_ascii(byte_data):
    """Convert byte data to ASCII values."""
    return [ord(byte) for byte in byte_data.decode(errors='ignore')]

def get_protocol_name(protocol_num):
    """Return the protocol name based on the protocol number."""
    if protocol_num == 6:
        return "TCP"
    elif protocol_num == 17:
        return "UDP"
    elif protocol_num == 1:
        return "ICMP"
    else:
        return f"Unknown ({protocol_num})"

def parse_pcap(pcap_file):
    """Parse the PCAP file and return packet information."""
    packets = rdpcap(pcap_file)
    packet_info = []

    for packet in packets:
        if packet.haslayer('IP') and packet.haslayer('TCP'):
            tcp_payload = packet['TCP'].payload  

            if tcp_payload:
                tcp_payload_bytes = bytes(tcp_payload)
                
                if len(tcp_payload_bytes) > 0 and any(byte != 0 for byte in tcp_payload_bytes):
                    ascii_values = bytes_to_ascii(tcp_payload_bytes)
                    info = {
                        'source': packet['IP'].src,
                        'destination': packet['IP'].dst,
                        'protocol': get_protocol_name(packet['IP'].proto),
                        'tcp_payload': tcp_payload_bytes.hex(),
                        'ascii_values': ascii_values
                    }
                    packet_info.append(info)
    return packet_info

def save_to_csv(packet_info, csv_file):
    """Save packet information to a CSV file."""
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['source', 'destination', 'protocol', 'tcp_payload', 'ascii_values'])
        writer.writeheader()
        writer.writerows(packet_info)
    print(f"Data saved to {csv_file}")

def main():
    """Main function to handle user interaction."""
    pcap_file = input("Enter the path to the PCAP file (e.g., 'file1.pcapng'): ")
    
    if not os.path.isfile(pcap_file):
        print(f"Error: The file '{pcap_file}' does not exist.")
        return

    packet_info = parse_pcap(pcap_file)

    if not packet_info:
        print("No packets found with TCP layer.")
        return

    base_name = os.path.splitext(os.path.basename(pcap_file))[0]
    csv_file = input(f"Enter the output CSV file name (default: 'Parse-{base_name}.csv'): ") or f"Parse-{base_name}.csv"

    save_to_csv(packet_info, csv_file)

if __name__ == "__main__":
    main()


# from scapy.config import conf
# conf.manufdb = "c:/users/mazay/desktop/kok iso/py/work/lib/python3.9/site-packages (1.1.5)/manuf"

# ("C:/Users/mazay/Desktop/Kok ISO/py/pcap1.pcapng")