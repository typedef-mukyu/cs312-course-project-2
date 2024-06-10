#!/bin/bash
yum install java -y
groupadd minecraft -r -U ec2-user
useradd mcsvc -M -r -s /usr/sbin/nologin -g minecraft
mkdir /minecraft
chown mcsvc:minecraft /minecraft/
chmod 775 /minecraft
mv /home/ec2-user/ec2setup-mcsvc.sh /
chmod 775 /ec2setup-mcsvc.sh
su mcsvc -s /bin/bash /ec2setup-mcsvc.sh
mv /home/ec2-user/minecraft.service /usr/lib/systemd/system/
chown root:root /usr/lib/systemd/system/minecraft.service
systemctl daemon-reload
systemctl enable minecraft
rm -f ~/ec2setup.sh /ec2setup-mcsvc.sh
reboot
