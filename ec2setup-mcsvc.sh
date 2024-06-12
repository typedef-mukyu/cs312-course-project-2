#!/bin/bash
cd /minecraft/
umask 002
echo "Downloading Minecraft Server 1.20.6..."
wget https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar
echo "Starting Minecraft Server..."
java -Xmx1024M -Xms1024M -jar server.jar nogui
echo "Accepting the EULA..."
echo "eula=true" > eula.txt
echo "Creating FIFO for server management..."
mkfifo serverinput