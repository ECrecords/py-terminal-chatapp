# Chat Application

A simple peer-to-peer chat application that uses sockets, selectors, and various commands to establish connections, send messages, and manage connections.

## Features

- Connect to other peers
- Send and receive messages
- List active connections
- Terminate connections
- Get local IP and port information
- Robust error handling

## Installation

```bash
git clone https://github.com/your-github-username/chat-application.git
cd chat-application
pip install -r requirements.txt
```

## Usage
To start the application:
```
python3 chat.py <port_number>
```
Available Commands:

- myip: Display your IP address.
- myport: Display the port the program is running on.
- connect <ip> <port>: Connect to another peer.
- send <id> <msg>: Send messages to peers.
- terminate <id>: End a peer connection.
- list: List active connections.
- exit: Exit the program.
- help: Display available commands.
