#!/usr/bin/env bash
# Written by shemhazai 0x00-0x00
# Downloads all dependencies

uid=$(id -u)
if [ "$uid" != "0" ]; then
    echo "You need administrative privileges to install python modules."
    exit
fi


echo "Read the README.md in the repository to find more information about module usage!"
sleep 1
echo "3 ..."
sleep 1
echo "2 ..."
sleep 1
echo "1 ..."
sleep 1

echo "[*] Trying to download dependencies..."
pip install rsa pycrypto gevent

echo "Bootstrap has terminated."

