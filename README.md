# POODLE Checker

Scan a netblock for SSLv3 enabled servers

# Setup

```apt-get install python3-pip
pip install IPy```

# Usage

```$ python3 sslcheck.py 10.0.1.0/24
10.0.1.1 [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:598)
10.0.1.2 timed out
10.0.1.3 timed out
10.0.1.4 SSLv3 enabled
10.0.1.5 SSLv3 enabled```
