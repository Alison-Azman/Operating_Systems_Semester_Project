# Chana Abbott
# Dr. Yitzchak Novick
# MCOO 243 - Operating Systems - SEMESTER PROJECT
# client.py
# Due Dec 13 2026

import socket
import sys
import threading
import time




#main method for thread that is receiving tasks from the user and sending them to the master
def send_jobs(client_socket, state, lock):
    job_id = 1
    while state["stay"]:
        task = get_task()
        send_task(task, job_id, client_socket)
        with lock:
            state["unfinished"] += 1
        job_id += 1
        again = submit_again()
        with lock:
            state["stay"] = again




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




#user can add jobs until he wants to stop
def submit_again():
    stay = input('Do you want to add another job? (y/n')
    while stay.lower() != 'y' and stay.lower() != 'n':
        stay = input("Please enter y or n")
    if stay.lower() == 'y':
        return True
    return False









#main method for thread that is receiving completed tasks from the master and responding to the user
def receive_jobs(client_socket, state, lock):
    with client_socket.makefile("r") as response_reader:
        more = True
        while more:
            with lock:
                more = True if state["stay"] or state["unfinished"] else False
            if more is False:
                return
            with lock:
                todo = state["unfinished"] > 0
            if not todo:
                time.sleep(0.01)
                continue
            received = receive_completion(response_reader)
            if not received:
                return
            with lock:
                state["unfinished"] -= 1




#respond to client
def receive_completion(response_reader):
    server_response = response_reader.readline().rstrip("\n")
    if not server_response:
        print("Connection to master closed")
        return False
    server_response = server_response.split('|')
    print(f"Task {server_response[1]} - job number {server_response[0]} complete!")
    return True






def main():
    state = {
        "stay": True,
        "unfinished": 0
    }

    if len(sys.argv) != 3:
        print("Usage: client.py <host name> <port number>", file=sys.stderr)
        sys.exit(1)

    host_name = sys.argv[1]
    port_number = int(sys.argv[2])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host_name, port_number))
            print("Connected successfully")

            lock = threading.Lock()
            send_thread = threading.Thread(target=send_jobs, args=[client_socket, state, lock])
            receive_thread = threading.Thread(target=receive_jobs, args=[client_socket, state, lock])

            send_thread.start()
            receive_thread.start()

            send_thread.join()
            receive_thread.join()





    except Exception as e:
        print("Exception:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
