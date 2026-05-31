# Detection and Prevention of Attacks During IoT OTA Firmware Updates Using Machine Learning and Deep Learning

## Overview

This repository contains the code, simulation tools, and experimental results associated with the MSc thesis:

**"Using Machine Learning and Deep Learning Solutions to Detect and Prevent Attacks During Firmware Updates in IoT"**

The thesis explores the security of Over‑the‑Air (OTA) firmware updates in Internet‑of‑Things (IoT) devices. It compares multiple machine learning and deep learning models on the public Edge‑IIoTset dataset, formalises the detection problem within the Neyman‑Pearson framework, and validates the findings through a custom, realistic OTA simulation that generates an independent dataset.

## Key Features

- **Formalised Detection Problem**: The detection task is cast as a Neyman‑Pearson hypothesis test, strictly controlling false alarms while maximising detection probability.
- **Model Benchmark**: Five classifiers (Random Forest, XGBoost, SVM, LSTM, CNN‑LSTM) and an attention‑based ensemble are evaluated on the Edge‑IIoTset dataset.
- **Lightweight & Real‑Time**: XGBoost achieves **0.9676 accuracy**, **0.9986 AUC**, and an inference time of **0.0135 ms per sample**, making it suitable for resource‑constrained IoT devices.
- **Realistic OTA Simulation**: A fully automated simulation built from scratch generates 3,600 enriched network sessions (Normal, DDoS, Intrusion, Backdoor, Reconnaissance, MITM) with background traffic (ARP, ICMP, DNS, MQTT).
- **Active Prevention Mechanism**: A four‑level alert system triggers proportional counter‑measures (log, notify, block IP, rollback firmware) based on model confidence.
- **Mixed‑Data Training**: Experiments show that even when 80 % of training data is simulated, accuracy remains > 0.93, proving that local adaptation requires very few real samples.

## Repository Structure
