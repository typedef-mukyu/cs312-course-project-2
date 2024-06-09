#!/usr/bin/python3
import os
import sys
import configparser
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
    print(awsCred.sections())
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
    os.system("terraform init > /dev/null")