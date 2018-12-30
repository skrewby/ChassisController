#!/bin/bash

function add_can_buses {
    echo "Creating virtual CAN..."
    ip link add vcan0 type vcan;
    ip link set vcan0 up;
    ip link add vcan1 type vcan;
    ip link set vcan1 up;
    ip link add vcan2 type vcan;
    ip link set vcan2 up;
    echo "
 Instructions:
  Listen        [candump -L vcan$]
  Send message  [cansend vcan$ <ID>#<MSG>]
 where 
  $             CAN bus number (0, 1 or 2)
  <ID>          hexadecimal COB-ID (ex. 10a)
  <MSG>         string message to send (ex. deadbeef)"
}

function remove_can_buses {
    echo "Removing virtual CAN"
    ip link delete vcan0;
    ip link delete vcan1;
    ip link delete vcan2;
}

function usage {
    echo -n "$(basename $0) [OPTION]

Setup a virtual CAN network consisting of 3 buses.

 Options:
  -r    Remove all the virtual CAN buses instead
"
}

# Script can only be run on sudo mode
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo: "
    echo "sudo $0 $*"
    exit 1
fi

# Make sure the can-utils package is installed first
if [ $(dpkg-query -W -f='${Status}' can-utils 2>/dev/null | grep -c "ok installed") -eq 0 ]; 
then
    apt-get install can-utils;
fi

# Execute the functions as required
if [ $# -eq 0 ]; then
    add_can_buses
elif [ $1 = "-r" ]; then
    remove_can_buses
else
    usage
fi
