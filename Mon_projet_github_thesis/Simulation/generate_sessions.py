import subprocess, os, time, traceback

BASE = r'C:\Users\papem\Desktop\OTA_simulation_IOT'
TSHARK = r'C:\Program Files\Wireshark\tshark.exe'
IFACE = '9'
REPEAT = 600  

scenarios = {
    'Normal':          ['python', 'client_normal.py'],
    'DDoS':            ['python', 'client_normal.py', '&', 'python', 'ddos_attack.py'],
    'Intrusion':       ['python', 'intrusion_attack.py'],
    'Backdoor':        ['python', 'client_backdoor.py'],
    'Reconnaissance':  ['nmap', '-sT', '-Pn', '-p', '1-1000', '127.0.0.1'],
    'MITM':            ['python', 'client_mitm.py']
}

for label, cmd in scenarios.items():
    print(f"\nGénération de {REPEAT} sessions {label}")
    for i in range(1, REPEAT + 1):
        pcap = os.path.join(BASE, f'session_{label}_enriched_{i}.pcap')

        # Si le fichier existe déjà et a une taille > 0, on le saute
        if os.path.exists(pcap) and os.path.getsize(pcap) > 0:
            print(f"  {label} {i}/{REPEAT} déjà existant, passage au suivant.")
            continue

        try:
            # Lance tshark en arrière-plan
            tshark_cmd = [TSHARK, '-i', IFACE, '-w', pcap]
            tshark_proc = subprocess.Popen(tshark_cmd, creationflags=subprocess.CREATE_NO_WINDOW)

            # Bruit protocolaire (avec timeout augmenté à 60s)
            for noise in ['arp_traffic.py', 'icmp_traffic.py', 'dns_traffic.py', 'mqtt_traffic.py']:
                subprocess.run(['python', noise], capture_output=True, text=True, cwd=BASE, timeout=60)
            time.sleep(0.5)

            # Scénario d'attaque / client
            subprocess.run(cmd, capture_output=True, text=True, cwd=BASE, timeout=120)

            # Arrêt de tshark
            tshark_proc.terminate()
            time.sleep(0.5)
            print(f"  {label} {i}/{REPEAT} terminé")

        except subprocess.TimeoutExpired as e:
            print(f"  ERREUR TIMEOUT sur {label} {i} : {e}")
            # On nettoie tshark
            try:
                tshark_proc.terminate()
            except:
                pass
            # On peut décider de continuer ou de s'arrêter ici (on continue)
        except Exception as e:
            print(f"  ERREUR sur {label} {i} : {e}")
            traceback.print_exc()
            try:
                tshark_proc.terminate()
            except:
                pass

print("\nFinalement termine.")