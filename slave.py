# Shaked Seller
# Dr. Yitzchak Novick
# MCOO 243 - Operating Systems - SEMESTER PROJECT
# slave.py
# Due Dec 13 2026

# Python socket reference sheets:
# https://www.w3schools.com/python/ref_module_socket.asp
# https://www.geeksforgeeks.org/python/socket-programming-python/

import socket
import sys
import time

def main():
    if len(sys.argv) != 4:
        print("Usage: slave.py <host name> <port number> <slave type>", file=sys.stderr)
        sys.exit(1)

    host_name = sys.argv[1]
    port_number = int(sys.argv[2])
    slave_type = sys.argv[3].upper()
    if not slave_type.isalpha or not len(slave_type) == 1:
        print("Invalid slave type.")
        sys.exit(1)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as slave_socket:
            slave_socket.connect((host_name, port_number))
            print("Connected successfully")
            slave_socket.sendall(f"{slave_type}\n".encode())

            job = slave_socket.recv(1024).decode()
            while job:
                job_parts = job.split("|")
                if job_parts[0] == "JOB":
                    job_id = job_parts[1]
                    job_type = job_parts[2]
                    print(f"Received JOB with ID {job_id} and TYPE {job_type}")

                    if slave_type == job_type:
                        process_time = 2
                    else:
                        process_time = 10

                    print(f"Processing JOB {job_id}...")
                    time.sleep(process_time)
                    print(f"JOB {job_id} complete.")
                    slave_socket.sendall((f"COMPLETE|{job_id}\n").encode())
                job = slave_socket.recv(1024).decode()



    except Exception as e:
        print("Exception:", e)
        sys.exit(1)

if __name__ == ("__main__"):
    main()
