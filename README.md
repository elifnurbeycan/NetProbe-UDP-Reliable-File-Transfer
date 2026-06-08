# NetProbe

Reliable UDP File Transfer and Network Performance Analysis System

## Features

- Reliable file transfer over UDP
- Sequence Number & ACK mechanism
- Timeout and Retransmission support
- Duplicate packet detection
- SHA-256 file integrity verification
- RTT, Throughput and Goodput analysis
- CSV-based logging
- Automatic graph generation
- Wireshark traffic monitoring support

## Technologies

- Python 3
- UDP Sockets
- SHA-256
- Pandas
- Matplotlib
- Wireshark
- Kali Linux (VMware)

## Run

### Start Server

```bash
python3 server.py
```

### Start Client

```bash
python3 client.py
```

### Run Analysis

```bash
python3 analysis.py
```

## Experiments

### ACK Loss Rate Analysis

- 0%
- 10%
- 20%
- 30%

### Packet Size Analysis

- 512 Bytes
- 1024 Bytes
- 2048 Bytes

## Metrics

- RTT
- Throughput
- Goodput
- Completion Time
- Retransmission Rate

## Project Structure

```text
NetProbe/
│
├── client.py
├── server.py
├── analysis.py
│
├── files/
│   ├── input/
│   └── received/
│
├── logs/
│   ├── transfer_log.csv
│   ├── experiment_results.csv
│   └── experiment_summary.csv
│
└── graphs/
```

## Authors

- Elif Nur Beycan
- Kübra Kaya
- Ceren Ebrar Yücetombullar

Computer Networks Project - 2026
