# Chana Abbott
# Dr. Yitzchak Novick
# MCOO 243 - Operating Systems - SEMESTER PROJECT
# client.py
# Due Dec 13 2026

import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: client.py <host name> <port number>", file=sys.stderr)
        sys.exit(1)

    host_name = sys.argv[1]
    port_number = int(sys.argv[2])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host_name, port_number))
            print("Connected successfully")
            job_id = 1
            with client_socket.makefile("r") as response_reader:
                task = input("What task do you want the system to accomplish? (A/B)").upper()
                while task != "A" and task != "B":
                    task = input("You must either choose task A or task B ").upper()
                send = f'{job_id}_{task}'
                job_id += 1
                client_socket.sendall((send + "\n").encode())
                print(f"Job {task} submitted successfully!")
                server_response = response_reader.readline().rstrip("\n")
                server_response = server_response.split('_')
                print(f"Task {server_response[1]} - job number {server_response[0]} complete!")


    except Exception as e:
        print("Exception:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()