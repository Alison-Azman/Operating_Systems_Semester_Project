
import socket
import threading
import sys

OPTIMAL_TIME = 2
NON_OPTIMAL_TIME = 10


#client connection
def handle_client(client_socket, request_reader, client_address, first_line):
   print(f"Client connected from {client_address}")
   handle_client_job(first_line, client_socket, client_address)


   for line in request_reader:
       line = line.rstrip("\n")
       if line:
           handle_client_job(line, client_socket, client_address)
   print(f"Client {client_address} disconnected")




#slave connections
#def handle_slave(slave_socket, request_reader, slave_type):




def handle_connection(conn_socket, address):
   try:
       with conn_socket, conn_socket.makefile("r") as request_reader:
           first_line = request_reader.readline().rstrip("\n")


           # Slave starts with A or B
           # Client job will start with ("JOB|id|type").
           if first_line.upper() in ("A", "B"):
               handle_slave(conn_socket, request_reader, first_line.upper())
           elif first_line.startswith("JOB|"):
               handle_client(conn_socket, request_reader, address, first_line)
           else:
               print(f"Unknown connection from {address}: \"{first_line}\"")
   except OSError as e:
       print(f"Connection with {address} ended: {e}")



def main():
    if len(sys.argv) != 2:
        print("Usage: master.py <port number>", file=sys.stderr)
        sys.exit(1)

    port_number = int(sys.argv[1])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as master_socket:
            master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            master_socket.bind(("", port_number))
            master_socket.listen()
            print(f"Master listening on port {port_number}")

            while True:
                conn_socket, address = master_socket.accept()
                threading.Thread(target=handle_connection, args=(conn_socket, address),
                                 daemon=True).start()

    except OSError as e:
        print(f"Exception caught when trying to listen on port {port_number} "
              f"or listening for a connection")
        print(e)


if __name__ == "__main__":
    main()
