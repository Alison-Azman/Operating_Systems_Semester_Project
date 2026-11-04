# Chana Abbott
# Dr. Yitzchak Novick
# MCOO 243 - Operating Systems - SEMESTER PROJECT
# client.py
# Due Dec 13 2026

import socket
import sys


#get a task from the user
def get_task():
    task = input("What task do you want the system to accomplish? (A/B)").upper()
    while task != "A" and task != "B":
        task = input("You must either choose task A or task B ").upper()
    return task



#send a job to the master
def send_task(task, job_id, client_socket):
    send = f'{job_id}|{task}'
    client_socket.sendall((send + "\n").encode())
    print(f"Job {task} submitted successfully!")



#respond to client
def receive_completion(response_reader):
    server_response = response_reader.readline().rstrip("\n")
    server_response = server_response.split('|')
    print(f"Task {server_response[1]} - job number {server_response[0]} complete!")



#user can add jobs until he wants to stop
def submit_again():
    stay = input('Do you want to add another job? (y/n')
    while stay.lower() != 'y' and stay.lower() != 'n':
        stay = input("Please enter y or n")
    if stay.lower() == 'y':
        return True
    return False



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
                stay = True
                while stay:
                    task = get_task()
                    send_task(task, job_id, client_socket)
                    job_id += 1
                    receive_completion(response_reader)
                    stay = submit_again()



    except Exception as e:
        print("Exception:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
