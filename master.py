# Alison Azman
# Chana Abbott
# Shaked Seller
# Dr. Yitzchak Novick
# MCOO 243 - Operating Systems - SEMESTER PROJECT
# master.py
# Due Dec 13 2026

import socket
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: master.py <host name> <port number>", file=sys.stderr)
        sys.exit(1)

    port_number = int(sys.argv[1])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as master_socket:
            master_socket.bind(("", port_number))
            master_socket.listen(1)

            slaves = {}
            for i in range(1):
                slave_socket, slave_address = master_socket.accept()
                slave_regis = (slave_socket.recv(1024).decode()).strip()
                slaves[slave_regis] = slave_socket
                print(f"Slave {slave_regis} connected successfully.")

            slaves["A"].sendall(("JOB|100|A\n").encode())
            print((slaves["A"].recv(1024).decode()).strip())
            slaves["A"].sendall(("JOB|200|B\n").encode())
            print((slaves["A"].recv(1024).decode()).strip())


    except Exception as e:
        print("Exception:", e)
        sys.exit(1)

if __name__ == ("__main__"):
    main()