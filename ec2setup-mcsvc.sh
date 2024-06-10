#!/bin/bash
cd /minecraft/
umask 002
wget https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar
java -Xmx1024M -Xms1024M -jar server.jar nogui
echo "eula=true" > eula.txt
mkfifo serverinput