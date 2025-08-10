#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#endif

int main() {
    // Server socket file descriptor
    SOCKET server_fd; // represents the server socket used to accept incoming connections
    
    // STRUCTURE TO HOLD SERVER ADDRESS INFO        AF_INET, IP, and port 
    // sockaddr_in is used for IPv4 addresses, sockaddr_in6 is used for IPv6 addresses
    struct sockaddr_in address;

    int opt = 1; // Option to set socket options, such as SO_REUSEADDR, allowing the socket to be reused
    
    int addrlen = sizeof(address); // Length of the address structure

#ifdef _WIN32
    // Initialize Winsock (Windows-specific)   
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        fprintf(stderr, "WSAStartup failed: %d\n", WSAGetLastError());
        return 1;
    }
#endif

    // 1. Create socket: IPv4, TCP 
    server_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); // address family, socket type(TCP), and protocol
    if (server_fd == INVALID_SOCKET) { // Check if socket creation was successful, INVALID_SOCKET indicates failure
        fprintf(stderr, "socket failed: %d\n", WSAGetLastError()); // Print error message 
        exit(EXIT_FAILURE); // Exit the program if socket creation fails
    }

    // 2. Set socket options (optional but recommended)
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, (const char *)&opt, sizeof(opt)); // file descriptor, level, option name, option value, and option length

    // 3. Define server address
    address.sin_family = AF_INET; // Address family: AF_INET for IPv4
    address.sin_addr.s_addr = htonl(INADDR_ANY); // Accept connections from any IP
    address.sin_port = htons(8080);       // Port 8080, hton= Host TO Network Short. converts to network byte order (big-endian)

    // 4. Bind socket to address
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) { // Bind the socket to the specified address and port
        fprintf(stderr, "bind failed: %d\n", WSAGetLastError()); // Print error message if binding fails
        closesocket(server_fd); // Close the socket if binding fails
        exit(EXIT_FAILURE); // Exit the program if binding fails
    }

    // 5. Listen for incoming connections
    if (listen(server_fd, 3) < 0) { // Listen for incoming connections, 3 is the backlog size
        fprintf(stderr, "listen failed: %d\n", WSAGetLastError()); // Print error message if listening fails
        closesocket(server_fd); // Close the socket if listening fails
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port 8080...\n");

    // 6. Accept a connection (blocking call)
    while (1) { // Infinite loop to accept multiple connections
        SOCKET new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen); // Accept an incoming connection, returns a new socket file descriptor for the accepted connection
        // address is the address of the connecting client, addrlen is the length of the address structure
        if (new_socket == INVALID_SOCKET) { // Check if accept was successful, INVALID_SOCKET indicates failure
            fprintf(stderr, "accept failed: %d\n", WSAGetLastError()); 
            continue; // Print error message and continue if accept fails
        }        
        printf("Connection accepted!\n");

        // Receive HTTP request from client (browser)
        char buffer[1024];
        int bytes_received = recv(new_socket, buffer, sizeof(buffer) - 1, 0); // Receive data from the client
        if (bytes_received > 0) {
            buffer[bytes_received] = '\0'; // Null-terminate the received data
            printf("Received request:\n%s\n", buffer); // Print the HTTP request
        }

        // Send HTTP response
        const char *body = "<h1>Hello, world!</h1>"; // HTML content to send
        char response[1024];
        snprintf(response, sizeof(response),
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Content-Length: %zu\r\n"
            "Connection: close\r\n"
            "\r\n"
            "%s", strlen(body), body); // Format the HTTP response with headers and body

        int bytes_sent = send(new_socket, response, (int)strlen(response), 0); // Send the response to the client
        if (bytes_sent == SOCKET_ERROR) {
            fprintf(stderr, "send failed: %d\n", WSAGetLastError()); // Print error if sending fails
        }
        
        send(new_socket, response, (int)strlen(response), 0); // Send the HTTP response to the client

        // 7. Close sockets
        closesocket(new_socket); // Close the client socket
    }
    // 8. Cleanup
    closesocket(server_fd);  // Close the server socket
    #ifdef _WIN32
    WSACleanup(); // Clean up Winsock
    #endif
    return 0;
}
