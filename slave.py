# Shaked Seller
# Dr. Yitzchak Novick
# MCOO 243 - Operating Systems - SEMESTER PROJECT
# slave.py
# Due Dec 13 2026

# Python socket reference sheets:
# https://www.w3schools.com/python/ref_module_socket.asp
# https://www.geeksforgeeks.org/python/socket-programming-python/
# Python thread reference sheets:

import sys
import socket
import time
from queue import Queue
import threading

def receive_jobs(slave_socket, slave_type, job_queue):
    with slave_socket.makefile("r") as job_reader:

        try:
            job = job_reader.readline().rstrip("\n")

            while job:
                job_parts = job.split("|")

                if job_parts[0] == "JOB":
                    job_id = job_parts[1]
                    job_type = job_parts[2]

                    job_queue.put((job_id, job_type))
                    print(f"Received JOB with ID {job_id} and TYPE {job_type}")

                job = job_reader.readline().rstrip("\n")

        finally:
            job_queue.put(None)

def process_jobs(job_queue, slave_type, slave_socket):
    while True:
        job = job_queue.get()
        if job is None:
            break

        next_job_id, next_job_type = job

        if slave_type == next_job_type:
            process_time = 2
        else:
            process_time = 10

        print(f"Processing JOB {next_job_id}...")
        time.sleep(process_time)
        print(f"JOB {next_job_id} complete.")

        slave_socket.sendall(
            f"COMPLETE|{next_job_id}\n".encode()
        )


def main():
    if len(sys.argv) != 4:
        print("Usage: slave.py <host name> <port number> <slave type>", file=sys.stderr)
        sys.exit(1)

    host_name = sys.argv[1]
    port_number = int(sys.argv[2])
    slave_type = sys.argv[3].upper()
    if slave_type not in ("A", "B"):
        print("Invalid slave type.")
        sys.exit(1)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as slave_socket:
            slave_socket.connect((host_name, port_number))
            print("Connected successfully")
            slave_socket.sendall(f"{slave_type}\n".encode())

            job_queue = Queue()

            r_thread = threading.Thread(target=receive_jobs, args=(slave_socket, slave_type, job_queue))
            p_thread = threading.Thread(target=process_jobs, args = (job_queue, slave_type, slave_socket))

            r_thread.start()
            p_thread.start()

            r_thread.join()
            p_thread.join()


    except Exception as e:
        print("Exception:", e)
        sys.exit(1)

if __name__ == ("__main__"):
    main()
