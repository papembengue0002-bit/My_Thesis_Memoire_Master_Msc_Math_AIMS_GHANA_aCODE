import subprocess
import pandas as pd
import numpy as np
import os
import glob

BASE_DIR = r'C:\Users\papem\Desktop\OTA_simulation_IOT'
TSHARK = r'C:\Program Files\Wireshark\tshark.exe'

FEATURES = [
    'arp.opcode','arp.hw.size','icmp.checksum','icmp.seq_le',
    'icmp.transmit_timestamp','http.content_length','http.response',
    'tcp.ack','tcp.ack_raw','tcp.checksum','tcp.connection.fin',
    'tcp.connection.rst','tcp.connection.syn','tcp.connection.synack',
    'tcp.dstport','tcp.flags','tcp.flags.ack','tcp.len','tcp.options',
    'tcp.payload','tcp.seq','tcp.srcport','udp.port','udp.stream',
    'udp.time_delta','dns.qry.name','dns.qry.name.len','dns.qry.qu',
    'dns.retransmission','dns.retransmit_request','mqtt.conflag.cleansess',
    'mqtt.conflags','mqtt.hdrflags','mqtt.len','mqtt.msgtype',
    'mqtt.proto_len','mqtt.topic_len','mqtt.ver'
]

AGG = {
    'arp.opcode':'sum', 'arp.hw.size':'sum',
    'icmp.checksum':'mean', 'icmp.seq_le':'mean','icmp.transmit_timestamp':'mean',
    'http.content_length':'mean', 'http.response':'first',
    'tcp.ack':'mean','tcp.ack_raw':'mean','tcp.checksum':'mean',
    'tcp.connection.fin':'sum','tcp.connection.rst':'sum',
    'tcp.connection.syn':'sum','tcp.connection.synack':'sum',
    'tcp.dstport':'mean','tcp.flags':'sum','tcp.flags.ack':'sum',
    'tcp.len':'mean','tcp.options':'mean','tcp.payload':'mean',
    'tcp.seq':'mean','tcp.srcport':'mean',
    'udp.port':'mean','udp.stream':'sum','udp.time_delta':'mean',
    'dns.qry.name':'first','dns.qry.name.len':'mean','dns.qry.qu':'mean',
    'dns.retransmission':'sum','dns.retransmit_request':'sum',
    'mqtt.conflag.cleansess':'sum','mqtt.conflags':'sum','mqtt.hdrflags':'sum',
    'mqtt.len':'mean','mqtt.msgtype':'sum','mqtt.proto_len':'sum',
    'mqtt.topic_len':'sum','mqtt.ver':'sum'
}

def extract_pcap(pcap_path):
    cmd = [TSHARK, '-o', 'http.tcp.port:5000', '-r', pcap_path, '-T', 'fields']
    for f in FEATURES:
        cmd.extend(['-e', f])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    lines = proc.stdout.strip().split('\n')
    data = [line.split('\t') for line in lines if line]
    if not data:
        return pd.DataFrame(columns=FEATURES)
    df = pd.DataFrame(data, columns=FEATURES)
    return df

def aggregate_flow(df):
    row = {}
    for col in FEATURES:
        mode = AGG.get(col, 'mean')
        series = df[col].dropna()
        if len(series) == 0:
            row[col] = 0 if mode != 'first' else ''
            continue
        try:
            series = pd.to_numeric(series, errors='coerce').dropna()
            if len(series) == 0:
                row[col] = df[col].iloc[0] if mode == 'first' else 0
                continue
            if mode == 'sum':
                row[col] = series.sum()
            elif mode == 'mean':
                row[col] = series.mean()
            elif mode == 'first':
                row[col] = df[col].iloc[0]
        except:
            row[col] = df[col].iloc[0] if mode == 'first' else 0
    return row

pcap_files = glob.glob(os.path.join(BASE_DIR, '*_enriched_*.pcap'))
all_rows = []
for pcap in pcap_files:
    parts = os.path.basename(pcap).split('_')
    label = parts[1]   
    if label == 'Recon':
        label = 'Reconnaissance'
    raw = extract_pcap(pcap)
    if raw.empty:
        print(f"  -> No packets in {pcap}, skipping")
        continue
    stats = aggregate_flow(raw)
    stats['label'] = label
    all_rows.append(stats)
    print(f"Processed {pcap}")

sim_enriched_df = pd.DataFrame(all_rows)
sim_enriched_df = sim_enriched_df[FEATURES + ['label']]
sim_enriched_df.to_csv('simulation_enriched.csv', index=False)
print(f'Enriched dataset created with {len(sim_enriched_df)} rows.')