import subprocess
TSHARK = r'C:\Program Files\Wireshark\tshark.exe'
cmd = [TSHARK, '-r', 'test_mqtt.pcap', '-T', 'fields', '-e', 'mqtt.msgtype', '-e', 'mqtt.topic']
proc = subprocess.run(cmd, capture_output=True, text=True)
for line in proc.stdout.strip().split('\n')[:5]:
    print(line)