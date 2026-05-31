import subprocess, os, time

BASE = r'C:\Users\papem\Desktop\OTA_simulation_IOT'
TSHARK = r'C:\Program Files\Wireshark\tshark.exe'
IFACE = '9'
REPEAT = 600

label = 'Reconnaissance'
print(f"Génération de {REPEAT} sessions {label}")

for i in range(1, REPEAT + 1):
    pcap = os.path.join(BASE, f'session_{label}_enriched_{i}.pcap')
    if os.path.exists(pcap) and os.path.getsize(pcap) > 0:
        print(f"  {label} {i}/{REPEAT} déjà existant, passé.")
        continue
    # Lancer tshark
    tshark_proc = subprocess.Popen([TSHARK, '-i', IFACE, '-w', pcap], creationflags=subprocess.CREATE_NO_WINDOW)
    # Bruits protocolaires
    for noise in ['arp_traffic.py', 'icmp_traffic.py', 'dns_traffic.py', 'mqtt_traffic.py']:
        subprocess.run(['python', noise], capture_output=True, text=True, cwd=BASE, timeout=60)
    time.sleep(0.5)
    # Scan nmap
    subprocess.run(['nmap', '-sT', '-Pn', '-p', '1-1000', '127.0.0.1'], capture_output=True, text=True, timeout=120)
    # Arrêter tshark
    tshark_proc.terminate()
    time.sleep(0.5)
    print(f"  {label} {i}/{REPEAT} terminé")

print("Génération Reconnaissance terminée.")