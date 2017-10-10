"""
To enable packet forwarding execute:
    echo 1 > /proc/sys/net/ipv4/ip_foward
"""
from scapy.all import *


def separator(ch, n):
    return ch*n


def process_pkt(pkt):
    raw = pkt.sprintf('%Raw.load%')
    match = re.search(r'\bGET\b|\bPOST\b', raw)

    if match:
        chunks = raw.split(r'\r\n')
        print '\n' + separator('-', 50)
        print '[+] {}'.format(chunks[0].split('\'')[1])
        for chunk in chunks[1:-2]:
            print '[+] {}'.format(chunk)


if __name__ == '__main__':
    print "[*] Waiting for packets..."
    sniff(filter='tcp', prn=process_pkt)
