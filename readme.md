# AWS EC2 Minecraft Server Automatic Install Script

## Introduction

This script deploys and installs a dedicated Minecraft (version 1.20.6) server on AWS,
running the application on an EC2 instance and creating the VPC infrastructure
necessary for outside players to connect to this server. An SSH key is also created
for remote management of this server.

This script works by first checking for the required AWS and Terraform CLIs, and
also checking for the AWS credential file mentioned below. The script will then read
the credentials file and set the corresponding environment variable for each credential.
`ssh-keygen` is then called to create a new SSH key pair for the server, and this script
reads the new public key file and generates a corresponding Terraform variable file
`sshkey.tf` to use that key with Terraform. The script then calls `terraform apply` to
provision the AWS resources, waits for the EC2 instance to become available, uses `scp`
to copy the `ec2setup.sh` and `ec2setup-mcsvc.sh` setup scripts along with the
`minecraft.service` service description file to the server. The script then uses `ssh`
to connect to the server and run the `ec2setup.sh` script as root (which then uses the
other two aforementioned files), which will create a service account with restricted
permissions, install the Minecraft server to the `/minecraft` directory, configure it to
run as a service under the restricted account, and restart the machine. After the server
is restarted, the script finishes by writing its public IP address to standard output.
A FIFO is also created in `/minecraft/serverinput` which links to the standard input
of the Minecraft server application for management. Users in the `minecraft` group can
execute server console commands by writing to that FIFO.

Note that it may take up to 3 minutes from when the script finishes for the server
to be available.

## Prerequisites

To run these scripts, you will need a Linux-based system with the following:

- AWS CLI (tested on version 2.16.4)
- Terraform CLI (tested on version 1.8.5)
- Python 3 (base installation, tested on 3.11.2)
- An OpenSSH installation with `ssh`, `scp`, and `ssh-keygen` (tested on OpenSSH 9.2p1)
- An AWS account with its credentials stored at `~/.aws/credentials`

Different versions of the above tools may work, but are not guaranteed to do so.

You should also review the [Minecraft end-user license agreement](https://www.minecraft.net/en-us/eula) before installing the server.

## Resources Created

This script will create the following AWS resources; their usage charges apply:

- One EC2 `t2.small` instance with Amazon Linux in the `us-west-2` region
- One VPC with the following:
  - The CIDR block of `10.3.12.0/24`
  - One Internet Gateway
  - One Route Table, with a main route table association
  - One subnet in availability zone `us-west-2a` with the CIDR block `10.3.12.0/28`, which automatically assigns public IP addresses
  - One security group that allows incoming SSH (port 22/TCP) and Minecraft (port 25565/TCP/UDP) traffic, as well as all outgoing traffic to pass
  - One network interface connecting the EC2 instance to the subnet mentioned above, with the aforementioned security groups

## Deployment

To create the server, simply run:

```
./main.py
```

This install script deploys the above resources and configures the server completely
automatically. Once the script completes, the server's public IP address will be 
written to standard output, while the server's SSH keys will be written to 
`~/.ssh/minecraftserver` (for the private key) and to `~/.ssh/minecraftserver.pub`
(for the public key).

**NOTE:** Ignore the errors displayed near the end of the script regarding `eula.txt`.
They are corrected immediately after they appear.

After the script completes, the EC2 instance may take a few minutes before it is
ready to accept Minecraft players.

## Management

Once the server is deployed, the SSH key at `~/.ssh/minecraftserver` can be used
to connect to the server with the username `ec2-user`:

```
ssh -i ~/.ssh/minecraftserver ec2-user@<ip-address>
```

The Minecraft server service can be managed as the systemd service `minecraft.service`.
For example, to restart the server:

```
sudo systemctl restart minecraft.service
```

The Minecraft server files are located at `/minecraft/`; any user in the `minecraft`
group can modify this directory, including the default `ec2-user`. 
Additionally, a FIFO that connects to the server's standard input is available at
`/minecraft/serverinput`; any user in the `minecraft` group can write to this to
execute server console commands. For example, the following can be used to kick the user `mcplayer`:

```
echo "/kick mcplayer" > /minecraft/serverinput
```

## Resources used

- AWS Learner Lab (for first manually creating the infrastrucure, then analyzing the created infrastructre to figure out what resources need to be created in this script)

- https://registry.terraform.io/providers/hashicorp/aws/latest/docs (for finding the corresponding Terraform code for each AWS resource)

- https://docs.python.org/3/library/configparser.html (for using the configparser Python library to parse the `~/.aws/credentials` file)

- https://www.freedesktop.org/software/systemd/man/255/systemd.service.html (for configuring ExecStop for the Minecraft systemd service)

- https://linux.die.net/man/1/bash (for writing Bash scripts and to implement read/write I/O redirection with the FIFO (since those block until both sides are opened))

- My original Course Project part 1 documentation (for commands needed to configure the EC2 instance, so those can be put into a script)