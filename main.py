#!/usr/bin/python3
import os
import sys
import configparser
from time import sleep
# Check for local machine prerequisites
def checkLocalPrereqs():
    print("Checking dependencies...")
    if os.system("which aws 2>&1 > /dev/null") != 0:
        print("\tAWS CLI: not found. Exiting...")
        exit(1)
    else:
        print("\tAWS CLI: OK")
    if os.system("which terraform 2>&1 > /dev/null") != 0:
        print("\tTerraform: not found. Exiting...")
        exit(1)
    else:
        print("\tTerraform CLI: OK")
    if os.system("test -e ~/.aws/credentials 2>&1 > /dev/null") != 0:
        print("\tAWS credentials: not found. Exiting...")
        exit(1)
    else:
        print("\tAWS credentials: OK")
def setEnvVars():
    awsCred = configparser.ConfigParser()
    awsCred.read(os.path.expanduser("~/.aws/credentials"))
    for k in awsCred["default"]:
        os.environ[k.upper()] = awsCred["default"][k]
def genPubKey():
    print("Generating SSH key pair to ~/.ssh/minecraftserver...")
    if(os.system("ssh-keygen -q -f ~/.ssh/minecraftserver -P \"\"") == 1):
        if os.system("test -e ~/.ssh/minecraftserver && test -e ~/.ssh/minecraftserver.pub"):
            print("Using existing key pairs.")
        else:
            print("Failed to create key pairs.")
            exit(1)
    with open(os.path.expanduser("~/.ssh/minecraftserver.pub")) as i:
        pubKey = i.read()
        with open("sshkey.tf", "w") as o:
            o.write("variable \"ssh_public_key\" {\n  description = \"SSH public key\"\n  type = string\n  default = \"")
            o.write(pubKey.strip("\n"))
            o.write("\"\n}")
def setUpTerraform():
    print("Initializing Terraform...")
    if os.system("terraform init > /dev/null") != 0:
        print("Terraform initialization failed.")
        exit(1)
    print("Creating AWS resources...")
    if os.system("echo \"yes\" | terraform apply") != 0:
        print("One or more AWS resources was not created successfully.")
        exit(1)
    print("All AWS resources were created succesfully.")
    os.system("terraform output > .output")
    with open(".output") as f:
        svrIP = f.read().split('"')[1]
        print("Server IP is %s" % svrIP)
    os.unlink(".output")
    return svrIP
def configureServer(ip: str):
    print("Waiting for EC2 instance to become ready...")
    while os.system("ssh -i ~/.ssh/minecraftserver -o StrictHostKeyChecking=accept-new ec2-user@%s cat /dev/null > /dev/null" % ip):
        sleep(1)
    print("Copying configuration scripts...")
    os.system("scp -i ~/.ssh/minecraftserver ./ec2setup.sh ./ec2setup-mcsvc.sh ./minecraft.service ec2-user@%s:~/" % ip)
    print("Running configuration scripts...")
    os.system("ssh -i ~/.ssh/minecraftserver ec2-user@%s sudo ./ec2setup.sh" % ip)
if __name__ == "__main__":
    checkLocalPrereqs()
    setEnvVars()
    genPubKey()
    ip = setUpTerraform()
    configureServer(ip)
    print("\nConfiguration complete. Server IP: %s" % ip)
