#!/usr/bin/env python3

import pyfiglet
import sys
import zmq
import json

from jsonrpcclient.requests import Request

ZMQ_SOCKET_ADDR = "tcp://127.0.0.1:4444"

def help():
    print(
    """
    ##### Help Text ######

    list -> List of all devices connected to server
    get_data_packet <device_addr_index> <timestamp> -> Fetch data packet with the given timestamp from device
    exit -> Exit comcon, go back to your world, lie down, have a cup of coffee, go to a spa.
    help -> Print this help text for your immediate rescue.
    """
    )


def list_devices(socket):
    print("List of devices connected to server.")
    socket.send_string("list")
    resp = socket.recv().decode('utf-8')
    devices = json.loads(resp)

    for i, dev in enumerate(devices):
        print(f"{i} -> {dev}")



def fetch_data_packet(socket, device_addr, timestamp):
    req = Request("get_data_packet", timestamp=timestamp)
    print(f"{device_addr} -> {req}")
    socket.send_string(str(req))
    resp = socket.recv().decode("utf-8")
    print(resp)

def send_to_device(socket, command):
    print("Sending a message to device.")

def main():
    print(pyfiglet.figlet_format("COMCON", font="slant"))
    print("Talk to end devices and control them by issuing commands.\n")

    #  Socket to talk to server
    print("Connecting to zmq socket")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(ZMQ_SOCKET_ADDR)

    help()

    try:
        while True:

            user_command = input("> ")

            if user_command.lower() == "list":
                list_devices(socket)
            
            elif user_command.startswith("send "):
                send_to_device(socket, user_command)
            
            elif user_command.startswith("get_data_packet"):
                parsed_user_command = user_command.strip().split(" ")
                
                device_addr = int(parsed_user_command[1])
                timestamp = int(parsed_user_command[2])
                
                fetch_data_packet(socket, device_addr, timestamp)
            
            elif user_command.lower() == "exit":
                print("\nBoi Boi")
                sys.exit(0)
            
            elif user_command.lower() == "help":
                help()
            
            else:
                print("Unknown command.")

    except KeyboardInterrupt:
        socket.disconnect(ZMQ_SOCKET_ADDR)
        print("\nBoi Boi")


if __name__ == "__main__":
    main()
