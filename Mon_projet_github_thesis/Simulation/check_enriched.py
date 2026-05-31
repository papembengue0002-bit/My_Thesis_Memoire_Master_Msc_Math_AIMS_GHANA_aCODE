import pandas as pd
import subprocess

TSHARK = r'C:\Program Files\Wireshark\tshark.exe'
PCAP = 'session_Normal_enriched_1.pcap'
features = ['arp.opcode', 'icmp.checksum', 'dns.qry.name']

cmd = [TSHARK, '-r', PCAP, '-T', 'fields']
for f in features:
    cmd.extend(['-e', f])

proc = subprocess.run(cmd, capture_output=True, text=True)
for line in proc.stdout.strip().split('\n')[:10]:
    print(line)