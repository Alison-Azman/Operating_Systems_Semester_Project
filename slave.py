# Shaked Seller
# Dr. Yitzchak Novick
# MCOO 243 - Operating Systems - SEMESTER PROJECT
# slave.py
# Due Dec 13 2026

import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: slave.py <host name> <port number>", file=sys.stderr)
        sys.exit(1)

    host_name = sys.argv[1]
    port_number = int(sys.argv[2])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as slave_socket:
            slave_socket.connect((host_name, port_number))
            print("Connected successfully")

    except Exception as e:
        print("Exception:", e)
        sys.exit(1)

if __name__ == ("__main__"):
    main()
