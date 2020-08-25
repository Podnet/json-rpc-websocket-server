#!/usr/bin/env python3

import pyfiglet
import sys
import zmq
import json


def help():
    print(
    """
    ##### Help Text ######

    list -> List of all devices connected to server
    send <device_ID> -> Send a command to a particular device
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

def send_to_device(socket, command):
    print("Sending a message to device.")

def main():
    print(pyfiglet.figlet_format("COMCON", font="slant"))
    print("Talk to end devices and control them by issuing commands.\n")

    #  Socket to talk to server
    print("Connecting to zmq socket")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:4444")

    help()

    try:
        while True:

            user_command = input("> ")

            if user_command.lower() == "list":
                list_devices(socket)
            
            elif user_command.startswith("send "):
                send_to_device(socket, user_command)
            
            elif user_command.lower() == "exit":
                print("\nBoi Boi")
                sys.exit(0)
            
            elif user_command.lower() == "help":
                help()
            
            else:
                print("Unknown command.")

    except KeyboardInterrupt:
        print("\nBoi Boi")


if __name__ == "__main__":
    main()
