#!/usr/bin/env python3

import pyfiglet
import sys


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


def list_devices():
    print("List of devices connected to server.")

def send_to_device(command):
    print("Sending a message to device.")

def main():
    print(pyfiglet.figlet_format("COMCON", font="slant"))
    print("Talk to end devices and control them by issuing commands.\n")

    help()

    try:
        while True:

            user_command = input("> ")

            if user_command.lower() == "list":
                list_devices()
            
            elif user_command.startswith("send "):
                send_to_device(user_command)
            
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
