#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#endif

int main() {
    // Server socket file descriptor
    int server_fd; // represents the server socket used to accept incoming connections
    
    // STRUCTURE TO HOLD SERVER ADDRESS INFO        AF_INET, IP, and port 
    //sockaddr_in is used for IPv4 addresses, sockaddr_in6 is used for IPv6 addresses
    struct sockaddr_in address;

    int opt = 1; // Option to set socket options, such as SO_REUSEADDR, allowing the socket to be reused
    
    int addrlen = sizeof(address); // Length of the address structure

    // 1. Create socket: IPv4, TCP 
    server_fd = socket(AF_INET, SOCK_STREAM, 0); // address family, socket type(TCP), and protocol
    if (server_fd == -1) { // Check if socket creation was successful, -1 indicates failure
        perror("socket failed"); // Print error message 
        exit(EXIT_FAILURE); // Exit the program if socket creation fails
    }

    // 2. Set socket options (optional but recommended)
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)); // file descriptor, level, option name, option value, and option length

    // 3. Define server address
    address.sin_family = AF_INET; // Address family: AF_INET for IPv4, 
    address.sin_addr.s_addr = INADDR_ANY; // Accept connections from any IP
    address.sin_port = htons(8080);       // Port 8080, hton= Host TO Network Short.cnvrts to network byte order (big-endian)

    // 4. Bind socket to address
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) { // Bind the socket to the specified address and port
        perror("bind failed"); // Print error message if binding fails
        close(server_fd); // Close the socket if binding fails
        exit(EXIT_FAILURE); // Exit the program if binding fails
    }

    // 5. Listen for incoming connections
    if (listen(server_fd, 3) < 0) { // Listen for incoming connections, 3 is the backlog size
        perror("listen failed"); // Print error message if listening fails
        close(server_fd); // Close the socket if listening fails
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port 8080...\n");

    // 6. Accept a connection (blocking call)
    int new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
    if (new_socket < 0) {
        perror("accept failed");
        exit(EXIT_FAILURE);
    }

    printf("Connection accepted!\n");

    // 7. Close sockets
    close(new_socket);
    close(server_fd);

    return 0;
}


